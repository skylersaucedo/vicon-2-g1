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
| [reports/g1_policy_data_scaling.md](reports/g1_policy_data_scaling.md) | Literature review of every learned policy embodied on a physical G1 (40 manuscripts, 22 with numeric hardware metrics): training data quantity versus hardware success, how many Vicon minutes a household task needs, and a protocol for measuring mocap minutes against normalized task completion. |
| [potential-manuscript-ideas.md](potential-manuscript-ideas.md) | Seven proposed experiments that the G1 literature has not run and that this lab can: a hardware mocap-minutes curve, a clips-versus-variants factorial, performer count, reference quality versus quantity, a Vicon-predicate benchmark with dataset release, first sweeping and dish-rack policies, and optical capture as a VLA demonstration source. Each with hypothesis, procedure, design diagram, budget, synthetic results showing what the data would look like under H1 and H0, and target manuscript. |
| [scripts/synthetic_results.py](scripts/synthetic_results.py) | Generates the seven `images/synthetic_e*.png` figures and `research_notes/synthetic_tables.md` from stated assumptions (seed 0). Not measured data. |
| [research_notes/g1_policy_data_scaling/](research_notes/g1_policy_data_scaling/) | Source notes behind the report: G1 tracking catalog, data-scaling evidence, G1 manipulation from demonstrations, learning-curve methodology. |
| [scripts/plot_data_vs_success.py](scripts/plot_data_vs_success.py) | Generates `images/g1_data_vs_success.png` from the hardware results tabulated in the report. |
| `images/` | Figures cropped from the PDFs and generated plots. |

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
3. [reports/g1_policy_data_scaling.md](reports/g1_policy_data_scaling.md): Tables 1 and 2, Figure 1, and the experiment section.
4. [ZEST](https://arxiv.org/pdf/2602.00401): Results; Materials and Methods.
5. [HuMBLE](https://arxiv.org/pdf/2610.10489): Supplementary Tables S3 to S9 for G1 parameters.

## Data quantity versus hardware success

Every published G1 hardware result with a trial count, plotted against the data unit each paper used. No G1 study uses minutes of motion capture as its axis; the only minutes-axis humanoid result is on an H1. Details, sources, and the proposed lab protocol are in [reports/g1_policy_data_scaling.md](reports/g1_policy_data_scaling.md).

![Hardware success versus training data on the Unitree G1](images/g1_data_vs_success.png)

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
- Data budget: a specialist box policy needs one to sixteen retargeted clips (under five minutes of post-retargeting motion); a generalist prior needs about three hours of curated capture. A mocap-minutes versus completion curve must be measured in the lab; the protocol is in the report (five nested data levels, seven policies, 315 scored rollouts, 105 to 175 GPU-hours).

## Open items

- Export a test take from Vicon as BVH; verify units, up-axis, and joint names against a GMR config.
- Stand up Isaac Lab or mjlab on the GPU machine; reproduce tracking of a HOLD box-lift clip in simulation.
- Fix the prop set (box dimensions and mass, broom, mock dishes) at 0.8 scale.
