# vicon-g1

Human-motion-to-humanoid skill transfer: capture household tasks (sweeping with a broom, picking up a box, washing dishes) with a Vicon optical motion capture system and train policies that a Unitree G1 executes autonomously.

## Contents

| File | Description |
|---|---|
| [literature_summary.md](literature_summary.md) | Summary of the four papers below: claims, methods, G1 results, metrics, and relevance to the goal. |
| [fbx_to_g1_policy_pipeline.md](fbx_to_g1_policy_pipeline.md) | Plan from a Vicon export to a deployed G1 policy: capture protocol, cleaning, retargeting, MDP configuration (gains, rewards, randomization, PPO), compute and schedule, deployment, pitfalls, measurement. |
| [manuscripts/2602.00401v1.pdf](manuscripts/2602.00401v1.pdf) | [ZEST: Zero-shot Embodied Skill Transfer for Athletic Robot Control](https://arxiv.org/abs/2602.00401) (RAI Institute, Boston Dynamics). The recipe being reproduced. |
| [manuscripts/2610.10489v1.pdf](manuscripts/2610.10489v1.pdf) | [HuMBLE: Human Motion-Driven Behavior Learning for Embodied Locomotion](https://arxiv.org/abs/2610.10489) (RAI Institute, Boston Dynamics). Same recipe; publishes the G1 configuration tables and the Vicon dataset. |
| [manuscripts/2603.14327v1.pdf](manuscripts/2603.14327v1.pdf) | [OmniClone: Engineering a Robust, All-Rounder Whole-Body Humanoid Teleoperation System](https://arxiv.org/abs/2603.14327) (BIGAI and partners). G1 pick-and-place via teleoperation and a GR00T VLA; stratified evaluation. |
| [manuscripts/2610.07891v1.pdf](manuscripts/2610.07891v1.pdf) | [Beyond Retargeting: Low-Latency and Robust Humanoid Whole-Body Teleoperation with Learned Atomic Motion Primitives](https://arxiv.org/abs/2610.07891) (HKUST, Zhejiang University, Tencent Robotics X). Robustness to noisy mocap input; success-rate definition. |
| [manuscripts/notes.txt](manuscripts/notes.txt) | Link to the [HOLD dataset](https://github.com/rai-opensource/hold): Vicon BVH locomotion and box-interaction clips released with HuMBLE, including G1 retargets. |
| `images/` | Figures cropped from the PDFs. |

## Pipeline

```mermaid
flowchart LR
    A["Vicon capture"] --> B["BVH export and cleaning"]
    B --> C["Scale, time-warp, retarget to G1 with GMR"]
    C --> D["PPO tracking policy<br/>Isaac Lab or mjlab"]
    D --> E["MuJoCo sim-to-sim"]
    E --> F["ONNX on G1 at 50 Hz"]
    F --> G["Scored trials in the Vicon volume"]
```

## Reading order

1. [literature_summary.md](literature_summary.md): Summary and side-by-side table.
2. [fbx_to_g1_policy_pipeline.md](fbx_to_g1_policy_pipeline.md): Sections 0, 5, and 8.
3. [ZEST](https://arxiv.org/pdf/2602.00401): Results; Materials and Methods.
4. [HuMBLE](https://arxiv.org/pdf/2610.10489): Supplementary Tables S3 to S9 for G1 parameters.

## Figures from the papers

**[ZEST](https://arxiv.org/abs/2602.00401), Figure 1.** Hardware deployment across data sources and robots. G1 clips: cartwheel and table tennis from mocap; ballet, jump onto box, climb up and down box from phone video.

![ZEST Figure 1: hardware deployment montage](images/zest_fig1_hardware.png)

**[ZEST](https://arxiv.org/abs/2602.00401), Figure 3.** Reference data and retargeting, PPO training with adaptive sampling and an assistive wrench, zero-shot deployment.

![ZEST Figure 3: framework overview](images/zest_fig3_overview.png)

**[HuMBLE](https://arxiv.org/abs/2610.10489), Figure 1.** Steerable locomotion on Atlas R1, Atlas D1, and Unitree G1 (row D: G1 walk-to-sprint; row E: box-parkour stack).

![HuMBLE Figure 1: hardware results](images/humble_fig1_hardware.png)

**[HuMBLE](https://arxiv.org/abs/2610.10489), Figure 6.** Teacher-student distillation followed by multi-task RL fine-tuning. The Stage I teacher is the ZEST tracker.

![HuMBLE Figure 6: two-stage framework](images/humble_fig6_framework.png)

**[OmniClone](https://arxiv.org/abs/2603.14327), Figure 1.** Stratified MPJPE on OmniBench and real-world G1 teleoperation.

![OmniClone Figure 1: benchmark and real-world overview](images/omniclone_fig1_overview.png)

**[OmniClone](https://arxiv.org/abs/2603.14327), Figure 3.** Model training (data recipe, teacher-student distillation) and system infrastructure (subject-agnostic retargeting, wireless transport, GR00T N1.6 as planner).

![OmniClone Figure 3: framework](images/omniclone_fig3_framework.png)

**[Beyond Retargeting](https://arxiv.org/abs/2610.07891), Figure 2.** Mixture-of-Experts teacher and codebook student mapping raw human motion plus proprioception to joint commands.

![Beyond Retargeting Figure 2: teacher-student framework](images/beyondretargeting_fig2_framework.png)

**[Beyond Retargeting](https://arxiv.org/abs/2610.07891), Figure 6.** G1 driven live by full-body optical motion capture.

![Beyond Retargeting Figure 6: optical mocap teleoperation](images/beyondretargeting_fig6_mocap_teleop.png)

## Decisions

- Architecture: single-skill motion-tracking policies in the ZEST style, one per captured clip. Box first, sweeping second, dish washing last with reduced scope.
- Tooling: [GMR](https://github.com/YanjieZe/GMR) for BVH-to-G1 retargeting; [BeyondMimic](https://github.com/HybridRobotics/whole_body_tracking) or [mjlab](https://github.com/mujocolab/mjlab) as the training base; MuJoCo for sim-to-sim checks; ONNX Runtime on the G1 Jetson for deployment.
- Compute: one 24 GB or larger NVIDIA GPU. An AWS g6e.8xlarge (one L40S, 48 GB) is sufficient; see pipeline Section 5.
- GR00T: not in phase one; see pipeline Section 0.
- Success metric: tracking success, tracking fidelity, and task outcome reported separately. The 0.8 task-completion target is scored on object outcome over at least 30 pre-registered hardware trials.

## Open items

- Export a test take from Vicon as BVH; verify units, up-axis, and joint names against a GMR config.
- Stand up Isaac Lab or mjlab on the GPU machine; reproduce tracking of a HOLD box-lift clip in simulation.
- Fix the prop set (box dimensions and mass, broom, mock dishes) at 0.8 scale.
