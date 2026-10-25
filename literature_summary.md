# Literature Summary: Human Motion Capture to Unitree G1 Policies

**Our goal.** Record household manipulation motions (sweeping with a broom, picking up a box, washing dishes) in our Vicon optical motion capture lab, and turn those recordings into a control policy that a Unitree G1 humanoid executes autonomously.

**Papers reviewed** (all in this folder):

| arXiv | Title | Group | Date |
|---|---|---|---|
| 2602.00401 | ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control | RAI Institute, Boston Dynamics | Jan 2026 |
| 2603.14327 | OmniClone: Engineering a Robust, All-Rounder Whole-Body Humanoid Teleoperation System | BIGAI, Peking University, and others | Mar 2026 |
| 2610.07891 | Beyond Retargeting: Low-Latency and Robust Humanoid Whole-Body Teleoperation with Learned Atomic Motion Primitives | HKUST, Zhejiang University, Tencent Robotics X | Oct 2026 |
| 2610.10489 | HuMBLE: Human Motion-Driven Behavior Learning for Embodied Locomotion | RAI Institute, Boston Dynamics | Oct 2026 |

Also referenced: the HOLD dataset repository in notes.txt (github.com/rai-opensource/hold), which is the Vicon dataset released alongside HuMBLE.

## The short version

All four papers share one recipe: retarget human motion to the robot skeleton, train a motion-tracking policy with reinforcement learning (PPO) in a massively parallel GPU simulator (Isaac Lab or Isaac Sim), and deploy to the G1 zero-shot through a joint-position PD controller at 50 Hz. Every one of them deploys on a real Unitree G1. That is good news for reproducibility.

The bad news: none of them does exactly what we want. Nobody records a manipulation task in a Vicon lab and then has the robot perform that task autonomously on objects. The closest is ZEST, which trains single-clip policies from Vicon mocap and video and deploys them on the G1, including box climbing with a real box. The others are teleoperation systems (OmniClone, Beyond Retargeting) or steerable locomotion (HuMBLE). The "task completion" numbers in these papers are almost all tracking success rates (the robot did not fall and stayed near the reference), not task outcome rates (the dirt got swept). Section 8 of the pipeline document (fbx_to_g1_policy_pipeline.md) covers how to close that gap.

**Relevance ranking for our project:** ZEST (highest), then HuMBLE (same group, same recipe, G1 details and Vicon dataset released), then OmniClone (shows pick-and-place on G1 and gives honest evaluation practice), then Beyond Retargeting (teleoperation robustness; least relevant to offline retraining).

---

## 1. ZEST: Zero-shot Embodied Skill Transfer (RAI Institute and Boston Dynamics)

**Claim.** One streamlined RL recipe trains single-skill motion-imitation policies from motion capture (Xsens and Vicon), monocular video, or keyframe animation, and deploys them zero-shot on Atlas, Unitree G1, and Spot. No contact labels, no observation history, no future-reference window, no state estimator, one set of hyperparameters per robot.

**What they did on the G1.** Cartwheel and table tennis from mocap. Ballet, jump onto box, climb up box, climb down box from phone video. The box skills are the most relevant to us: the policy interacts with a physical object using proprioception only (no box perception). They randomize the robot's initial pose relative to the box during training so the policy tolerates placement error. Box climb up and climb down succeeded 5 of 5 consecutive hardware trials at the nominal setup, and all trials inside the training distribution (plus or minus 10 cm in x, plus or minus 0.3 rad in yaw) succeeded. The policy also survived a 2 kg torso payload and box heights outside the training range.

**Method essentials.**
- Observations: IMU angular velocity, gravity direction, joint positions, joint velocities, previous action, plus only the next reference frame (base height, base linear and angular velocity, gravity direction, reference joint positions).
- Actions: residual offsets added to the reference joint positions, sent to a PD controller. Residual actions beat absolute actions decisively in ablation.
- Rewards: exponential-kernel tracking of base pose, base velocities, joint positions, and key-body poses; regularization on action rate, joint acceleration, and joint and torque limits; constant survival bonus. Nothing task-specific.
- Asymmetric actor-critic: the critic sees privileged simulation state (base velocity, contact forces, key-body positions).
- Adaptive reference-state initialization: clips are cut into 4 s bins, each bin tracks a failure level, and resets are biased toward hard bins.
- Assistive wrench curriculum: a model-based virtual force and torque on the torso that decays automatically as tracking improves. Needed for acrobatic clips, often removable for simpler ones.
- Domain randomization kept moderate: friction, plus or minus 10 percent link mass, impulsive pushes, observation noise.
- PD gains chosen analytically from joint armature values for the parallel-linkage ankles and knees. Same gains in sim and on hardware.

**Compute.** Each policy: about 10 hours (7k PPO iterations) on a single NVIDIA L4 GPU with 4096 parallel environments in Isaac Lab. Single-skill policies were used for all hardware results because they outperform a multi-skill policy at a fixed training budget.

**Data pipeline.** Vicon and Xsens exported to BVH, retargeted in two stages (human skeleton to a robot-proportioned proxy skeleton, then to the robot) via a spacetime optimization that also jointly solves a uniform scale and time resampling so ballistic phases stay consistent with real gravity. Video clips go through MegaSaM plus TRAM to recover SMPL motion, then the same retargeting. Converting a clip takes minutes; "capture in the morning, train during the day, run it on hardware that evening."

**Metrics.** Hardware: mean absolute joint error MAE(q), mean angular distance of base orientation MAD(R), mean L2 base angular velocity error, and the maxima of each, over successful trials. Simulation: success rate over 10,000 randomized rollouts per clip, reported as mean, 10th percentile, and minimum.

**Relevance to us: highest.** This is the recipe to reproduce. It consumes Vicon mocap directly, deploys on the G1, and handles object interaction with a fixed object through pose randomization. Gaps: code is not released, the retargeter is proprietary, and the household tasks involve held tools (broom) and many small objects (dishes) that the paper never touches.

---

## 2. OmniClone: All-Rounder Whole-Body Humanoid Teleoperation (BIGAI and partners)

**Claim.** A single transformer tracking policy, trained on a carefully balanced 30-hour motion dataset on one RTX 4090, lets operators of any height teleoperate a G1 through dynamic motions and precise loco-manipulation. The same policy executes generated motions and serves as the low-level controller under a Vision-Language-Action (VLA) model.

**What they did on the G1.** Real-time teleoperation of a G1-Comp (29 DoF plus 12 DoF Inspire hands, RealSense head camera) through a pick-and-place, opening a cabinet and retrieving a tissue, serving tea without spilling, transporting coffee beans, and running. Six operators from 1.47 m to 1.94 m succeeded within 5 to 7 practice trials. They collected 50 teleoperated demonstrations and post-trained NVIDIA GR00T N1.6 to run autonomously: 85.71 percent success on pick-and-place (21 trials) and 80 percent on squat-to-pick-and-place (5 trials).

**Method essentials.**
- Teacher-student: a privileged teacher trained with PPO (about 60 hours, 33k steps, 4096 envs), then a student distilled with DAgger (about 22 hours) that sees only deployable observations plus a few future reference frames. Total about 80 GPU hours on one RTX 4090.
- Transformer backbone beat an MLP in every category under identical training.
- OmniBench: a diagnostic benchmark of unseen generated motions in six categories (loco-manipulation, manipulation, squatting, walking, running, jumping), each stratified by height or speed, 60 episodes per category. Aggregate metrics hide failures; stratified ones expose them.
- Data recipe: roughly 60 percent standing manipulation, the remaining 40 percent split between dynamic and stable locomotion. Small changes to that minority fraction, and filtering of biased sequences, steer the policy's behavior strongly.
- Subject-agnostic retargeting: a dynamic scale factor computed from a calibration frame removes per-operator calibration. They measured up to 20 cm skeletal scale discrepancies between capture systems and subjects, worth about 20 mm of tracking error.
- Infrastructure: FIFO frame buffer with zero-order hold, UDP transport, about 80 ms end-to-end latency.

**Metrics.** Success rate (percent of episodes without failure) and mean per-joint position error (MPJPE) in millimeters, stratified by category and difficulty, evaluated in MuJoCo on motions not in training. Real-world: operator task completion after practice; VLA task success rate.

**Relevance to us: medium.** Not an offline retraining paper, but it demonstrates pick-and-place on a G1 with hands and gives the most honest evaluation methodology of the four. Two reusable lessons: stratify your evaluation, and treat dataset composition as a first-class design variable. It also offers an alternative route if direct mocap tracking of dish washing proves infeasible: teleoperate the G1 with our Vicon system, record demonstrations, and train a VLA.

---

## 3. Beyond Retargeting: Retargeting-Free Teleoperation with a Motion Codebook (HKUST, Zhejiang, Tencent)

**Claim.** Skip online retargeting entirely. A student policy maps raw human keypoints plus robot proprioception straight to G1 joint commands in one forward pass. A factorized discrete codebook of motion primitives snaps noisy, partial, or out-of-distribution human observations onto plausible full-body prototypes, which makes the policy far more robust than a continuous MLP student.

**What they did on the G1.** One checkpoint drives a real G1 from four input sources without fine-tuning: a VR headset (head and wrists only), a full-body optical mocap system, monocular video via GVHMR, and text-to-motion output from HY-Motion. Demonstrated motions: arm raises, punches, bending, squatting, walking, lateral stepping, and a bimanual grasp-turn-squat-place via VR.

**Method essentials.**
- Stage 1: privileged Mixture-of-Experts teacher trained with PPO on 14,147 retargeted AMASS, LAFAN1, and OMOMO clips with adaptive sampling.
- Stage 2: student with a 128-channel by 12-entry codebook, trained by matching codes from corrupted inputs to codes from clean inputs, plus action distillation and auxiliary heads.
- Training-time augmentation: random keypoint masking and noise so the student handles sparse inputs.

**Metrics.** Success rate defined as finishing the reference clip without the pelvis height error ever exceeding 0.25 m. Seven tracking errors (MPJPE in rad, velocity errors, root errors) with fixed penalties substituted for failed frames to avoid survivorship bias. Robustness sweeps over dropout, keypoint noise, root-height drift, initialization bias, and unseen motions. End-to-end latency measured from video by aligning optical flow of the operator and the robot (147.5 ms median on hardware). On the held-out set the codebook student reached 95.90 percent success versus 84.51 percent for TWIST.

**Relevance to us: low to medium.** It is a teleoperation paper and the retargeting-free design is irrelevant to an offline pipeline where retargeting cost does not matter. Still useful for three things: a crisp, reusable success-rate definition; the warning that real sensing (including optical mocap) is noisier than the clean training distribution, so inject noise and dropout during training; and evidence that Mixture-of-Experts teachers and adaptive sampling matter when tracking large, diverse libraries.

---

## 4. HuMBLE: Human Motion-Driven Behavior Learning for Embodied Locomotion (RAI Institute and Boston Dynamics)

**Claim.** From about three hours of Vicon locomotion capture, train a compact MLP that produces human-like, fully steerable walking from only proprioception and a planar velocity command. Deployed on Atlas R1, Atlas D1, and Unitree G1; shown live at CES 2026.

**What they did on the G1.** Joystick-steered walking through sprinting with emergent gait transitions, outdoor deployment, and integration as the locomotion layer under a box-parkour planner (the climbing experts are ZEST-style policies). G1 inference is 1.1 ms on the Jetson AGX Orin CPU via ONNX Runtime.

**Method essentials.**
- Stage 1: a ZEST-style full-body tracking teacher, distilled with DAgger into a command-conditioned prior.
- Stage 2: multi-task RL fine-tuning with half the environments tracking references (style regularizer) and half tracking random velocity commands (coverage). Goal-conditioned reference-state initialization seeds rollouts from dataset frames with similar commands. Critic warm-started from the teacher critic for 5000 iterations before the actor is unfrozen.
- Vicon details: 120 Hz, subject-calibrated rig, gap filling and filtering, export to BVH, two-stage retargeting as in ZEST, mirroring across the sagittal plane, and estimated sole and toe bones added to fix ambiguous foot contact.
- Scaling for the G1: the actor averaged 178 cm; the G1 is about 0.8 of that. They scale lengths by 0.8 and time by 1 over the square root of 0.8 so gravity stays 9.81 m/s squared in the scaled data.
- G1 hardware lessons: ankles came out too stiff and stumbled on real floors until they added terrain roughness randomization (plus or minus 2.5 cm) in the second half of teacher training. The G1 state estimator drifts outdoors, so they also trained a variant without the linear velocity observation.

**Metrics.** Fidelity to the reference measured as DTW-aligned mean absolute error of torso velocities and joint positions, normalized by the reference's own standard deviation. Steady-state command-tracking error and 90 percent rise time over a grid of velocity commands. Push-recovery envelopes. Sim-versus-real error tables on identical command sequences.

**Released artifacts.** HOLD dataset (CC-BY-4.0): 552 BVH trajectories, about 576 minutes at 120 Hz, including the 0.8-scaled variant and example G1 retargeted motions. Beyond locomotion it contains lifting, carrying, and pushing boxes, stepping onto boxes, and sitting. The paper says the G1 reference motion dataset and figure data will be released.

**Relevance to us: high as a reference, low as a target.** We do not need steerable locomotion. But this is the same group and recipe as ZEST, it exposes the full G1 training configuration (PD gains, action scales, domain randomization ranges, termination thresholds, PPO hyperparameters) that ZEST only summarizes, and the HOLD dataset includes Vicon box-lifting and box-carrying clips already retargeted to the G1. Those clips are a free validation set for our retargeting and training pipeline before we touch our own captures.

---

## Side-by-side

| | ZEST | OmniClone | Beyond Retargeting | HuMBLE |
|---|---|---|---|---|
| Input to deployed policy | Full-body reference, next frame only | Reference plus future frames (teleop stream) | Raw human keypoints, no retargeting | Planar velocity command |
| Human data source | Vicon, Xsens, phone video, animation | AMASS, LAFAN, TWIST2 corpus, own teleop (30 h) | AMASS, LAFAN1, OMOMO (14k clips) | Own Vicon capture (3 h) |
| Policy | MLP, single skill per policy | Transformer, one policy for everything | MLP student with discrete codebook; MoE teacher | MLP, two-stage with fine-tuning |
| Training stages | 1 (PPO) | 2 (PPO teacher, DAgger student) | 2 (PPO teacher, distillation) | 3 (PPO teacher, DAgger prior, PPO fine-tune) |
| Simulator | Isaac Lab | Isaac Lab (train), MuJoCo (eval) | Isaac Sim (train), MjLab (eval) | Isaac Lab (train), MuJoCo (cross-check) |
| Compute reported | 10 h per skill, 1 x NVIDIA L4 | 80 h, 1 x RTX 4090 | Not stated | Not stated |
| G1 object interaction | Box climb, jump onto box (proprioception only) | Pick-and-place, cabinet, tea (teleop and VLA) | Bimanual grasp via VR | Box climb as separate expert |
| Success metric | Sim success over 10k rollouts; hardware N of N trials | Stratified success rate and MPJPE on unseen motions | Clip completed with pelvis height error under 0.25 m | DTW-aligned MAE, command error, push envelope |
| Code released | No | Pipeline "will be released" | Not stated | Dataset only (HOLD) |

## What this means for our plan

1. **Reproduce ZEST, informed by HuMBLE's G1 tables.** Single-skill tracking policies, one per clip, trained in Isaac Lab (or MuJoCo Warp via mjlab) for about 10 GPU-hours each. The open BeyondMimic and mjlab codebases implement the same family of recipe for the G1 and are the practical starting point since ZEST code is closed.
2. **Start with the box.** Picking up a box is the only one of our three tasks that any paper comes close to (ZEST box interaction, HOLD box-lifting clips). Sweeping adds a held tool. Dish washing adds water, deformables, slippery contacts, and fine finger control that none of these papers attempt with a tracking policy.
3. **Expect to define task completion ourselves.** The papers measure "did the robot keep tracking without falling." We care whether the box moved. Our Vicon system can measure both: put markers on the G1 and the objects and compute global tracking error and object outcome in the same coordinate frame. No paper here has that capability on hardware.
4. **Fallback path.** If direct mocap tracking fails for dishes, OmniClone shows a G1 can be teleoperated through the task with optical mocap as the input, demonstrations recorded, and a VLA trained with roughly 50 demonstrations.
