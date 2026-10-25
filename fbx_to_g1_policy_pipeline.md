# From Vicon FBX to a Deployed Unitree G1 Policy

A practical, end-to-end plan for turning a motion capture recording of a household task (sweep with a broom, pick up a box, wash dishes) into a reinforcement-learning policy that runs on a Unitree G1. Every design choice below is taken from the four papers in this folder (ZEST, OmniClone, Beyond Retargeting, HuMBLE) unless marked as our own inference. Section 7 collects the warnings and best practices; Section 8 covers measurement.

## 0. Pick the architecture before capturing anything

| Option | What the deployed policy receives | Papers | Fit for our tasks |
|---|---|---|---|
| A. Single-skill tracker, one policy per clip | Proprioception plus the next reference frame | ZEST | Best first target. Simplest, fastest to train, proven on G1 with a physical box. |
| B. Multi-skill tracker, one policy for a library | Proprioception plus reference frames | BeyondMimic, OmniClone teacher, Beyond Retargeting teacher | Second step once A works for each task. ZEST found single-skill policies track better at a fixed budget. |
| C. Teleoperation plus VLA | Operator stream, then camera plus language | OmniClone | Fallback for dish washing if tracking a fixed clip is too brittle. |
| D. Command-conditioned (steering) | Velocity or sparse goal command | HuMBLE | Not needed for our tasks now. Relevant later if the robot must walk to the sink. |

![HuMBLE Figure 6: Stage I teacher-student distillation and Stage II multi-task fine-tuning](images/humble_fig6_framework.png)

*HuMBLE, Figure 6. Option A is the Stage I teacher alone (the ZEST tracker). Options B and D add the distillation and fine-tuning stages shown here.*

**Recommendation.** Option A for all three tasks, starting with the box. Treat sweeping as the second task and dish washing as a stretch goal with a reduced scope (dry mock dishes, no water).

![OmniClone Figure 3: training pipeline and system infrastructure with GR00T N1.6 as planner](images/omniclone_fig3_framework.png)

*OmniClone, Figure 3. Option C. GR00T N1.6 sits above the tracking policy as a high-level planner; the tracking policy is still required underneath.*

**Do we need GR00T?** Not for Options A, B, or D. GR00T N1.6 is a vision-language-action model: it consumes camera images, language, and robot state from demonstrations, and it does not ingest motion capture. OmniClone used it only in Option C, post-training on 50 teleoperated demonstrations (4 x A100, 20k steps, batch 384) and running it on top of its own tracking policy as the low-level controller. Two consequences for us. First, a working whole-body tracking policy is a prerequisite for GR00T on a G1 either way, so Option A comes first regardless. Second, GR00T becomes worth running only when we hit one of two triggers: a tracking policy completes the box task but cannot generalize to object placement beyond the randomized range, or dish washing proves too brittle to track from a fixed clip and we fall back to teleoperation. If we reach that point, community reports indicate N1.6 fine-tunes on a single 48 GB card (L40, L40S, A6000) at reduced batch size; check the current Isaac-GR00T hardware notes before committing.

## 1. Capture protocol in the Vicon lab

What HuMBLE and ZEST did, plus what our tasks require.

**Rig and rate.**
- 120 Hz capture (HuMBLE). Subject-calibrated skeleton with full range-of-motion calibration before every session.
- Full-body marker set that resolves hands and feet well. Wrist orientation matters: all four papers track wrist key-bodies, and OmniClone and Beyond Retargeting treat wrist orientation as a first-class input.
- Fingers: optional. No paper tracks finger motion from mocap; the G1 hand (Dex3 or Inspire) is commanded separately or left in a fixed grasp. Capture a few finger markers only if we plan a scripted open or close.

**Actor.**
- The G1 is about 1.2 m and 35 kg. HuMBLE's actor averaged 178 cm and they scaled all lengths by 0.8 for the G1. A shorter actor needs less scaling, but any actor works if we scale correctly in step 3. Record the actor's height and limb lengths.
- OmniClone measured up to 20 cm skeletal scale discrepancies between capture setups and subjects, which cost about 20 mm of tracking error. Keep one actor per task to start.

**Props.** Put rigid-body marker clusters on every object the robot will touch: the box, the broom handle, each dish, the sink rim or table edge. HOLD recorded box and chair props as separate bones with corner offsets so object size and pose are in the same BVH as the skeleton. We need the object trajectory to (a) place the object in simulation at the right pose and size and (b) score task completion later (Section 8).

**Choreography (ZEST and HuMBLE conventions).**
- Every take starts and ends in a quiet standing pose. ZEST's policies all begin and return to standing. This gives the robot a safe reset.
- 5 to 17 second clips. ZEST's hardware skills were 4 to 17 s. Longer is fine with adaptive sampling but trains slower.
- Repeat each task 5 to 10 times with small natural variation (box position, sweep direction). Variation across takes is what we will randomize over in simulation.
- Slow, deliberate, and symmetric. The G1 has lower torque and a worse IMU than Atlas (ZEST attributes higher orientation error on G1 to IMU quality). Avoid fast arm swings near joint limits and deep crouches below 0.5 m torso height (HuMBLE's G1 fall threshold).
- Keep feet planted or take clear, deliberate steps. Shuffling, sliding feet produce ambiguous contact that HOLD had to fix with estimated sole bones.
- Mark the capture volume floor and keep the actor away from the edges to avoid occlusion gaps.

**Volume and scale.** Scale the scene for the robot, not the human. If the box will sit on a 0.4 m stool for the robot, the actor lifts from 0.5 m (0.4 divided by 0.8). Same for the sink height and the broom length (a child's broom at 0.8 scale). Mismatched object scale is a retargeting problem no optimizer can fully fix.

## 2. Export and clean

**Export format.** BVH, not FBX, wherever possible. Every paper here consumed BVH (ZEST, HuMBLE, HOLD, LAFAN1). The open GMR retargeter reads BVH natively, while its FBX path requires the Autodesk FBX SDK Python bindings in a separate environment and a two-step import. If Vicon Shogun or Nexus gives us FBX only, convert to BVH in Blender (import FBX, export BVH with Z-up, meters) and check joint names and the rest pose.

**Checks on export.**
- Units in meters, Z-up, right-handed, consistent with the G1 model. Vicon defaults to millimeters.
- Frame rate recorded in the file header. HOLD's scaled files change the frame time rather than resampling; our retargeter must read the header, not assume 30 or 120 Hz.
- Root joint is the pelvis and the skeleton has no leaf bones the retargeter will not understand.

**Cleaning (HuMBLE and HOLD procedure).**
1. Gap-fill missing markers with interpolation constrained by the skeleton.
2. Low-pass filter high-frequency marker noise. Keep it light; ZEST's reward tolerates noise and heavy filtering destroys the heel-toe details that make motion look human.
3. Estimate the ground plane and foot soles. HOLD detects double-support frames by foot velocity and height thresholds and fits a constant heel and toe pose so that stationary feet sit at z = 0 with gravity aligned. Do this before scaling, because foot penetration and floating after retargeting are the most common cause of policies that learn to stomp or hover.
4. Mirror each take across the sagittal plane (HuMBLE, HOLD). Doubles the data and gives left-handed and right-handed versions of sweeping for free. Mirror the object trajectories too.
5. Trim to the start-standing and end-standing frames.

## 3. Retarget to the G1 (29 DoF)

**Scale and time-warp first.** Uniformly scale all lengths by s = robot height over actor height (about 0.8 for a 1.5 m actor, 0.67 for a 1.8 m actor; ZEST picks s by matching thigh length). Then stretch time by 1 over the square root of s. Both ZEST and HuMBLE do this so gravity stays 9.81 m/s squared under the scaled kinematics; HuMBLE found that skipping the time warp visibly hurt training on anything with a flight phase. Our tasks have no flight phase, but lifting dynamics still change with scale. Scale the object trajectories and dimensions by the same s.

**Retargeter.** ZEST and HuMBLE use an in-house spacetime optimization (not released) in two stages: human skeleton to a robot-proportioned proxy skeleton with spherical joints, then proxy to robot, with alignment frames on head, torso, upper arms, lower arms, hands, pelvis, knees, and feet, joint-velocity regularization, and non-penetration constraints with self and ground. The practical open equivalent is General Motion Retargeting (GMR, MIT license, github.com/YanjieZe/GMR), which:
- has a BVH configuration for the 29 DoF G1 (`unitree_g1`) and a 43 DoF variant with hands,
- was tuned specifically so RL tracking policies train well on its output (foot sliding and self-penetration were the artifacts it was built to remove),
- outputs per-frame base translation, base rotation, and joint positions as a pickle, with a script to convert to the CSV layout BeyondMimic expects.

Our BVH joint names will not match the LAFAN1 or Nokov presets, so expect to write one GMR IK config mapping our Vicon skeleton to the G1 and to spend a day tuning weights.

**Quality gate before training.** Replay the retargeted clip in simulation kinematically (BeyondMimic's `replay_npz.py` or GMR's viewer) and check:
- no foot sliding during stance, no ground penetration, no self-collision (hands through thighs during a squat are common),
- joint angles inside G1 limits with margin, joint velocities under the actuator limits,
- the hands reach the scaled object pose within a few centimeters. If they do not, fix scale, not reward weights.

**Objects in the reference.** The policy will not see the object (ZEST box climb is proprioception-only). The object's role is in simulation: a rigid body of the right size and mass placed at the captured relative pose, with its initial pose randomized (ZEST used plus or minus 10 cm and plus or minus 0.3 rad for the box and a height range of 0.70 to 0.80 m). For the broom, model it as a rigid stick attached to the hand (welded or held with a high-friction fixed grasp) in the first iteration; a free broom that must be grasped is a separate, harder problem.

## 4. Simulation and MDP setup

![ZEST Figure 3: reference data, training setup with adaptive sampling and assistive wrench, zero-shot deployment](images/zest_fig3_overview.png)

*ZEST, Figure 3. Everything in this section configures the middle block: PPO in Isaac Lab with an asymmetric critic, time-binned adaptive sampling, and the assistive wrench curriculum.*

**Simulator.** Isaac Lab (ZEST, HuMBLE, OmniClone, BeyondMimic). The MuJoCo Warp alternative, mjlab (Apache 2.0), reuses the Isaac Lab manager API and ships a G1 tracking task; BeyondMimic's maintainers moved to it. Pick one and also set up plain MuJoCo for sim-to-sim validation, as OmniClone, HuMBLE, and Beyond Retargeting all did.

**Starting codebase.** BeyondMimic's `whole_body_tracking` (MIT, archived but complete) or mjlab's `Mjlab-Tracking-Flat-Unitree-G1`. Both implement the DeepMimic-family recipe for the G1 and accept retargeted CSV motions through a Weights and Biases registry. We then modify them toward the ZEST configuration below.

**Robot model.** Unitree's G1 29 DoF description. Set joint armature values for the knee and ankle parallel linkages (ZEST shows these dominate the PD response) and use HuMBLE's published G1 gains (Table S7 of that paper):

| Joint | Kp | Kd | Nominal angle (rad) | Action scale |
|---|---|---|---|---|
| Waist roll, pitch | 150 | 3.0 | 0 | 0.1 |
| Waist yaw | 100 | 2.0 | 0 | 0.1 |
| Hip roll, yaw | 40 | 3.0 | 0 | 0.2, 0.1 |
| Hip pitch | 40 | 3.0 | -0.1 | 0.2 |
| Knee | 80 | 2.5 | 0.2 | 0.2 |
| Ankle roll | 40 | 2.0 | 0 | 0.05 |
| Ankle pitch | 40 | 2.0 | -0.1 | 0.2 |
| Shoulder roll | 20 | 1.0 | 0.25 left, -0.25 right | 0.1 |
| Shoulder pitch, yaw | 20 | 1.0 | 0.1, 0 | 0.1 |
| Elbow | 30 | 1.0 | 1.0 | 0.1 |
| Wrist roll, pitch, yaw | 20 | 0.5 | 0 | 0.01 |

Use identical gains in simulation and on the robot. For manipulation we will likely raise the wrist action scale above 0.01, since HuMBLE's value is for walking.

**Timing.** Physics at 250 Hz (dt 0.004 s), control decimation 5, policy at 50 Hz (ZEST). Episode cap 10 s with reference-state initialization so long clips still get covered.

**Observations (ZEST actor).** Torso angular velocity, gravity vector in torso frame, joint positions, joint velocities, previous action, plus the next reference frame: base height, base linear velocity, base angular velocity, gravity direction in base frame, reference joint positions. No history stack, no future window (both hurt in ZEST's ablation), no estimated base linear velocity (drifts on the G1 per HuMBLE). Gaussian observation noise: 0.10 on angular velocity, 0.015 on gravity, 0.005 rad on joints, 0.25 rad/s on joint velocities.

**Critic (privileged).** Everything the actor sees plus true base linear velocity and height, contact forces, key-body positions and velocities relative to base, assistive wrench, tracking rewards, and phase. For our object tasks, add object pose relative to the robot to the critic only.

**Actions.** Residual joint targets: command equals reference joint position plus action scale times policy output. Not absolute targets.

**Rewards (ZEST Table S4; HuMBLE adds the regularizers in italics).** Tracking terms use exp(-k times squared error over sigma squared) with k = 0.25:

| Term | Sigma or weight |
|---|---|
| Base position | 0.4 |
| Base orientation | 0.5 |
| Base angular velocity | 1.5 |
| Base linear velocity | 0.6 |
| Joint positions | 0.3 times square root of joint count |
| Key-body positions (relative to base) | 0.2 times square root of key-body count |
| Key-body orientations | 0.4 times square root of key-body count |
| Action rate penalty | 0.15 |
| Joint acceleration penalty | 1e-5 |
| Joint limit penalty | 1.0 |
| Torque limit penalty | 0.1 |
| Survival bonus per step | 1.0 |
| *Foot slide, foot jerk, foot clearance (HuMBLE)* | *tune* |

For the box task, add nothing object-specific at first. ZEST climbed a box with the generic reward; the key-body terms on hands and feet already encode the contact.

**Terminations (HuMBLE G1 values).** Contact force above 6000 N, torso height deviation from reference above 0.3 m, torso tilt deviation above 0.6 rad, body-ground penetration above 0.03 m, foot self-collision.

**Reference-state initialization and adaptive sampling.** Reset to a random phase of the clip; bin the clip into 4 s windows; maintain an EMA (alpha 0.005) of failure per bin; sample bins with a softmax over failure with a 15 percent uniform floor. Mandatory once we train on several takes or a long clip.

**Assistive wrench curriculum.** Model-based PD force and torque on the torso scaled by beta up to 0.6 (ZEST) or 0.75 (HuMBLE), decayed as tracking improves. For slow household motions it may be unnecessary; keep it available for the squat-to-lift.

**Domain randomization (ZEST and HuMBLE G1 ranges).**

| Term | Range |
|---|---|
| Static friction | U(0.6, 1.3) |
| Dynamic friction | U(0.5, 0.9) |
| Restitution | U(0.0, 0.2) |
| Link mass scale | U(0.9, 1.15) |
| Torso center of mass offset | plus or minus 2.5 cm x, plus or minus 5 cm y and z |
| Joint friction | ankle U(0, 0.05), waist U(0, 0.1) |
| Joint zero offset | plus or minus 0.03 rad ankle, plus or minus 0.015 rad others |
| Impulsive push on base | every U(0, 10) s, up to 0.3 m/s (G1) |
| External force and torque on torso | plus or minus 5 N, plus or minus 5 N m, every 2 to 4 s |
| Initial pose and velocity perturbation | plus or minus 0.1 m, 0.1 rad, 0.1 m/s; joints plus or minus 0.2 rad, 0.5 rad/s |
| Terrain roughness | plus or minus 2.5 cm, introduced after mid-training (HuMBLE, to soften G1 ankles) |
| Object initial pose (ours, after ZEST) | plus or minus 10 cm, plus or minus 0.3 rad yaw; object mass plus or minus 20 percent |

Keep it moderate. ZEST warns that excessive randomization makes policies conservative or aggressive.

**PPO (ZEST Table S7).** Actor MLP 512-256-128 ELU, critic 512-512-256 ELU, empirical observation normalization, learning rate 1e-3 adaptive on KL with target 0.01, gamma 0.99, GAE lambda 0.95, clip 0.2, entropy 0.001, 5 epochs, 4096 environments, 24-step rollouts, 4 mini-batches. HuMBLE uses a larger 1024-512-256 actor for a three-hour dataset; the smaller one is enough for one clip.

## 5. Compute, time, and budget

**Reported numbers.**

| Paper | Hardware | Time | What was trained |
|---|---|---|---|
| ZEST | 1 x NVIDIA L4 (24 GB) | about 10 h, 7k iterations | one single-skill G1 or Atlas policy |
| ZEST ablation | same | 20 h, 14k iterations | 15-motion multi-skill Atlas policy |
| OmniClone | 1 x RTX 4090 (24 GB) | 60 h teacher plus 22 h student | 30-hour-dataset transformer tracker |
| OmniClone VLA | 4 x A100 | 20k steps | GR00T N1.6 post-training on 50 demos |
| HuMBLE | not stated | 3 stages; 5000-iteration critic warm start alone before fine-tuning | locomotion prior and fine-tune |

**Our estimate (inference, not from the papers).**
- GPU: one 24 GB class card is enough for 4096 G1 environments in Isaac Lab or mjlab. An RTX 4090, L4, L40S, or A6000 all fit. Two cards let us run a box policy and a sweep policy in parallel. No multi-node training is needed.
- CPU and RAM: Isaac Lab wants a modern 8-core or better CPU and 32 GB RAM; 64 GB is comfortable with Isaac Sim loaded.
- Per task: expect 3 to 6 training runs of 8 to 12 hours each before a policy is worth putting on hardware (reward tuning, object randomization, retargeting fixes). That is 30 to 70 GPU-hours per task, 100 to 200 GPU-hours for all three. On a cloud L4 at a few USD per hour this is in the hundreds of USD; a local 4090 pays for itself within the project.
- Sim evaluation: ZEST's 10,000 randomized rollouts per clip take minutes at 4096 environments.
- Onboard inference: trivial. HuMBLE measured 1.1 ms for an MLP on the G1's Jetson AGX Orin CPU with ONNX Runtime. A ZEST-size MLP is smaller.

**AWS option: g6e.8xlarge.** One NVIDIA L40S (48 GB, Ada generation, RTX-class), 32 vCPUs, 256 GiB RAM, roughly 4.5 USD per hour on demand in us-east-1 (about 3.4 USD per hour on a one-year savings plan, 1.8 USD per hour spot at the time of writing; verify on the AWS pricing page). This exceeds every requirement above:
- ZEST's reference GPU was an L4 (24 GB). The L40S has twice the memory and several times the throughput, so a 10-hour ZEST run should finish in well under 10 hours or can run 8192 environments.
- Isaac Sim and Isaac Lab require an RTX-class NVIDIA GPU and run headless on EC2; the L40S qualifies. mjlab (MuJoCo Warp) has no such restriction.
- 32 vCPUs and 256 GiB cover Isaac Sim's CPU-side asset loading comfortably.
- Cost at our estimate of 100 to 200 GPU-hours: 450 to 900 USD on demand, under 400 USD on spot with checkpointing. One training run per policy is about 45 USD.
- The one limitation is a single GPU, so box and sweep policies train sequentially rather than in parallel. Launch a second instance if the schedule needs it.
- Keep the 10,000-rollout evaluation and MuJoCo sim-to-sim on the same instance; both are cheap. ONNX export and deployment need no GPU.

**Calendar (inference).**

| Phase | Duration | Exit criterion |
|---|---|---|
| Tooling: Isaac Lab or mjlab plus BeyondMimic G1 task running on a HOLD or LAFAN1 clip | 1 to 2 weeks | Policy tracks a public clip in sim with over 95 percent success under randomization |
| Vicon capture, export, cleaning, GMR config for our skeleton | 1 to 2 weeks | Retargeted clip passes the kinematic quality gate |
| Box pick-up: train, iterate, sim-to-sim in MuJoCo | 2 to 3 weeks | Over 90 percent sim success with object randomization; passes MuJoCo replay |
| Hardware bring-up: ONNX export, SDK deployment, air replay without object, then with object | 1 to 2 weeks | 5 of 5 nominal trials (ZEST's bar) |
| Sweeping, then dishes | 3 to 4 weeks each | Same gates |

## 6. Deployment on the G1

![ZEST Figure 1: hardware deployment montage including G1 box climbing, ballet, cartwheel, and table tennis](images/zest_fig1_hardware.png)

*ZEST, Figure 1. The G1 box skills in the middle rows are the closest published precedent for our object tasks: proprioception only, box pose randomized during training, 5 of 5 nominal hardware trials.*

- Export the actor to ONNX from the training checkpoint along with its observation normalization statistics. ZEST logs checkpoint plus metadata to a registry and configures the hardware controller from that metadata automatically; copy that habit so the sim and robot configs cannot diverge.
- Run the policy at 50 Hz on the Jetson via ONNX Runtime, sending joint position targets to the Unitree low-level PD loop with the same Kp and Kd as in simulation.
- Observations come straight from the IMU and joint encoders. No state estimator is needed with the ZEST observation set. Yaw is not observed or tracked; the IMU yaw drifts (ZEST).
- Playback: the retargeted reference is a lookup table indexed by time since the start button. Start the robot in the standing pose the clip starts from, standing at the captured relative pose to the object (use floor tape, or our Vicon system itself to place the robot).
- Safety: gantry or harness with slack for the first trials, operator on the emergency stop, start from zero-torque to PD hold at the nominal pose, then start the clip. Verify in MuJoCo sim-to-sim first; HuMBLE describes MuJoCo as a hardware-validated proxy.
- Validate with the robot in the Vicon volume (markers on pelvis, torso, hands, feet, and object). This gives us a ground-truth global trajectory the papers did not have.

## 7. Things to consider and avoid (as stated by the papers)

**Data and retargeting**
- Scale space and time together. Spatial scaling alone changes effective gravity and degrades training (HuMBLE, ZEST).
- Do not label contacts. ZEST's reward never uses contact schedules and that is why it survives noisy references.
- Fix feet on the ground before training (HOLD's estimated sole bones). Floating or penetrating feet teach stomping.
- Expect the human scale discrepancy to show up as tracking error; compute scale from a calibration frame rather than trusting the capture system's skeleton (OmniClone).
- Keep clips starting and ending in standing (ZEST).
- Composition matters more than volume once you have more than one clip. OmniClone steered an entire policy's behavior by changing the minority fraction of its dataset and by filtering a few biased sequences. If we train a multi-task policy later, balance box, broom, and dish clips deliberately.

**MDP design**
- Residual actions, not absolute (ZEST's worst ablation).
- No observation history and no future reference window with an MLP (ZEST: both degrade, history more sharply). OmniClone's transformer student does use future frames, but that is a different architecture and a teleoperation setting.
- Keep privileged information in the critic (ZEST: stripping it degrades value estimates).
- One generic reward for all skills. Do not add per-task shaping until the generic one fails (ZEST, HuMBLE's teacher).
- Moderate domain randomization (ZEST). Add terrain roughness late in training to soften G1 ankles (HuMBLE).
- Adaptive sampling is what makes long clips (ZEST table tennis) and multi-clip libraries learn evenly. Without it the hard phases stay weak.
- Single-skill policies beat a multi-skill policy at a fixed budget (ZEST). Do not start with one policy for all three tasks.

**G1 hardware specifics**

![Beyond Retargeting Figure 6: G1 driven live by full-body optical motion capture](images/beyondretargeting_fig6_mocap_teleop.png)

*Beyond Retargeting, Figure 6. A G1 driven live from optical mocap. Their robustness sweeps are the evidence that real mocap streams are noisier than the clean clips a tracker trains on; the same applies to our offline references.*

- The G1 IMU is noisier than Atlas's; expect higher base-orientation error (ZEST).
- The G1 state estimator's linear velocity drifts; do not feed it to the policy (HuMBLE's velocity-free variant, ZEST's observation set).
- Model the knee and ankle parallel linkages with armature values and derive PD gains from them (ZEST, HuMBLE).
- Real objects differ from simulated ones in compliance and friction (ZEST's box). Randomize those too, and prefer stiff, high-friction props in the lab at first.
- Policies invariant to lateral offset still fail outside their randomized x and yaw range (ZEST Figure S5). Randomize at least the placement error we can realistically guarantee on the floor.

**Task-specific warnings (our inference)**
- Sweeping: model the broom as held, not grasped, in version one. Floor contact of the bristles is a compliant, sliding contact no paper here simulates.
- Dishes: none of the papers handle water, deformables, or slippery wet surfaces, and none track fingers from mocap. Start with dry rigid mock dishes moved from one rack to another, and plan on OmniClone's teleoperation plus VLA route if tracking is too brittle.
- Box: ZEST randomized box height 0.70 to 0.80 m and robot start pose; its policy generalized to 0.55 m. Expect similar generalization on pick-up height but not on box width, which changes the grasp.

## 8. Measuring success

### How the authors measure it

Nobody in these papers scores whether the task was accomplished in the physical world. They score whether the robot tracked the reference without failing.

| Paper | Primary success metric | Secondary | Where |
|---|---|---|---|
| ZEST | Success rate: fraction of 10,000 randomized rollouts per clip that are not early-terminated (contact force over threshold or large deviation from reference). Reported as mean, 10th percentile, and minimum across clips. | MAE of joint angles, mean angular distance of base roll and pitch, mean L2 base angular velocity error, plus the maxima; all over successful trials only | Simulation for success rate; hardware for tracking errors and N of N trial counts (5 of 5 for box climb) |
| Beyond Retargeting | Success: the rollout reaches the end of the reference clip without the pelvis height error ever exceeding 0.25 m | Seven tracking errors with fixed penalty values substituted for failed frames so that a policy that falls early is not rewarded by a short, clean trajectory | Cross-simulator (trained in Isaac Sim, evaluated in MjLab) on 6,495 out-of-distribution clips |
| OmniClone | Success rate per category and difficulty (18 cells, 60 episodes each) on unseen generated motions; and MPJPE in millimeters | Real-world: six novice operators complete a walk-stabilize-pick-and-place within 5 to 7 practice trials; VLA success 18 of 21 and 4 of 5 | MuJoCo for the benchmark; hardware for operator and VLA trials |
| HuMBLE | DTW-aligned mean absolute error of torso velocities and joint positions against the reference, normalized by the reference standard deviation (the deployment policy sat at 0.15 to 0.26 standard deviations) | Steady-state command error, 90 percent rise time, push-recovery envelope, sim-versus-real error tables | Simulation plus hardware for the sim-to-real tables |

A "0.8 task completion score" in this literature therefore means: 80 percent of rollouts finished the clip without triggering a fall or deviation termination. OmniClone's 80 percent number is the only one that is a real task outcome, and it rests on 5 trials.

### What we should measure, and how to demonstrate 0.8

**Define three layers and report all three.**

1. **Tracking success (the papers' metric).** A trial succeeds if the policy runs to the end of the clip with no fall, no emergency stop, pelvis height error under 0.25 m (Beyond Retargeting) or torso height deviation under 0.3 m and tilt under 0.6 rad (HuMBLE's G1 thresholds). Compute in simulation over thousands of randomized rollouts and on hardware per trial.
2. **Tracking fidelity.** On hardware, ZEST's MAE(q) and MAD(R) from the robot's own joint encoders and IMU. With the robot inside the Vicon volume we can add what the papers could not: global root position error and hand position error against the reference, time-aligned with DTW as in HuMBLE. Report these only over successful trials and say so.
3. **Task outcome (ours).** Binary per trial, scored from Vicon object markers and a human judge:
   - Box: box lifted at least 15 cm above its support, carried, and released with its center within 10 cm of the target footprint, upright, with no drop.
   - Sweep: broom bristles in contact with the floor along at least 80 percent of the reference sweep path, and a measured pile of light debris (dry rice or foam pellets) displaced at least X cm toward the target line. Choose X from a human baseline run.
   - Dishes: each mock dish moved from the source rack to the destination rack without falling to the floor.

   **Task completion score = successful task outcomes divided by total attempted trials, counting falls and aborts as failures.** Do not condition on tracking success.

**Trial protocol for a defensible 0.8.**
- Pre-register the protocol: object placement tolerance, number of trials, success definitions, and what counts as an abort.
- Run two conditions, following ZEST: nominal (object at its training-nominal pose, robot placed by floor markers) and perturbed (object offset sampled uniformly within the training randomization range, plus 2 kg torso payload for one subset).
- Trials: 20 consecutive nominal trials and 20 perturbed trials per task. At 16 of 20 successes the point estimate is 0.80 but the 95 percent Wilson interval is roughly 0.58 to 0.92. To claim the score is at least 0.8 with reasonable confidence, run 30 trials and require 27 or more (interval lower bound about 0.74) or 50 trials with 44 or more. Five trials, as in ZEST's box test or OmniClone's squat task, demonstrate feasibility, not a rate.
- Consecutive, not best-of. ZEST reported five consecutive runs. Report every trial, including the ones after a battery swap.
- Gate hardware trials on simulation: at least 0.95 success over 10,000 randomized rollouts and a passing sim-to-sim replay in MuJoCo before the first hardware attempt. ZEST's hardware policies came from sim success rates above 0.9; a 0.8 target in the real world is unrealistic from a policy below 0.9 in sim.
- Record and publish the per-trial table and video, with tracking error alongside the outcome. OmniClone's lesson is that an aggregate 0.8 hides which conditions fail; stratify by condition.

**Demonstration staircase.** Each step is a milestone the team can show:
1. Public clip (HOLD box lift or LAFAN1 walk) tracked in sim above 0.95 success.
2. Our Vicon clip retargeted and tracked in sim above 0.95 success with object randomization.
3. Air replay on the real G1 with no object: 10 of 10 completions.
4. Nominal object trials: 16 of 20 or better.
5. Perturbed object trials: 16 of 20 or better. This is the 0.8 we can publish.

## References to tooling

- HOLD dataset (Vicon, BVH, G1 retargets, CC-BY-4.0): github.com/rai-opensource/hold
- General Motion Retargeting (BVH and FBX to G1, MIT): github.com/YanjieZe/GMR
- BeyondMimic G1 tracking in Isaac Lab (MIT, archived): github.com/HybridRobotics/whole_body_tracking
- mjlab, MuJoCo Warp successor with a G1 tracking task (Apache 2.0): github.com/mujocolab/mjlab
- Isaac Lab (NVIDIA), MuJoCo (DeepMind) for sim-to-sim checks
