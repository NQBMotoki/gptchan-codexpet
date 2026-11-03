# GPT酱动作确认记录（2026-11-02）

用户查看现有九种动作预览后，确认除跳跃外的八种动作可纳入正式使用。下表固定的是本机／仓库 `1.2.0-dev.1` 的对应动作行，而不是此前被认为画风过浓的注视组试作。

确认时的基准图集：[1.2.0-dev.1 图集](../art/animation/v1.2.0-dev-20261102/spritesheet.webp)，文件 SHA-256：`b3a521ed88820aa4d5aa2d7bf70f003fbcec6c7ea36f398f4a5f0abdfd3307aa`。下表的行哈希是将整个 1536×208 行按 RGBA 解码后的像素字节计算的 SHA-256，包含该行透明空格；可用来确认后续修改没有改变已确认的动作。

| 动作 | 图集行（从 0 开始） | 帧数 | 预览 | 解码行 SHA-256 |
| --- | ---: | ---: | --- | --- |
| 待机 | 0 | 6 | [待机](../assets/readme/animations/idle.gif) | `7d0ad2113a7ebf9967ded0055e1266e73ebcdbc7e13ea307f3a7e8704f74dc1b` |
| 向右移动 | 1 | 8 | [向右移动](../assets/readme/animations/running-right.gif) | `a8cc6cce727caa024129d19940dfa15c05646652f17ff711ce290f6066827734` |
| 向左移动 | 2 | 8 | [向左移动](../assets/readme/animations/running-left.gif) | `94acdcf1c3dbafc36192f411f7e598665f27f94b4c945a83550c1cebff156afa` |
| 挥手 | 3 | 4 | [挥手](../assets/readme/animations/waving.gif) | `4e810e54d093432eec56b2b53decee19e4f09ba051c0861da7f6fd19c43b2db5` |
| 失败 | 5 | 8 | [失败](../assets/readme/animations/failed.gif) | `9947d6ceedfb8192fbcc601f7c3e133ccdc15ccc77e27b67fe2050dcacfb2d5c` |
| 等待 | 6 | 6 | [等待](../assets/readme/animations/waiting.gif) | `bf4e6ed0252a55857178d3c63cc59813580d5a561d96d2194dd509778f548384` |
| 工作 | 7 | 6 | [工作](../assets/readme/animations/running.gif) | `0b17d463c302339004691b7309cf9e3bc3b75d9855b1f292258e2186098878f5` |
| 复核 | 8 | 6 | [复核](../assets/readme/animations/review.gif) | `d4bf82395da6494d062886b31add8737931ffc3a39efb3ec3a16b83e73fcac29` |

## 当前安装与待处理部分

- 当前仓库图集中，上述八个动作行与以上基准的解码像素一致；新的原地扇翼占用跳跃行。GIF 的播放速度仅供审样，不代表宿主实际表现。
- 2026-11-02 从当时云端 GPT酱 重新下载图集并按解码 RGBA 像素比较：上述八个动作中，除工作行动画为旧版外，其余七行与当时本机完全一致；当时云端跳跃也与本机不同。后续同步状态以 2026-11-03 的实际操作记录为准。
- `jumping` 槽位已按用户后续讨论重新制作：原地站稳、正面看向用户、双手背在身后，以舒缓节奏大幅扇动双翼，身体自然起伏、尾巴轻摆；不额外增加特效。见 [生成与检查记录](../art/animation/jump-grounded-20261102/README.md)。
- 十六向注视属于另外两行，不属于本次确认的九种动作。使用者于 2026-11-03 另行审看并接受 Candidate 08，详见 [注视审看](ANIMATION-REVIEW-20261103.md)。
- 宿主中的动作触发、循环节奏与真实桌面缩放效果由用户实测；图集结构或预览本身不代表这些检查已完成。
