# GPT酱 1.1.0-dev 动画审看

制作与检查：2026-10-26 至 27。九状态关键姿势已获使用者认可，本轮完成整套可安装候选动画，保留同一 `gpt-chan` 身份及 `classic` 经典白紫礼服。未新增安静版／表现版，也未将同一套衣服登记成多个版本。

## 查看成品

- [九状态连续预览 GIF](../art/animation/v2/previews/final/all-states.gif) / [MP4](../art/animation/v2/previews/final/all-states.mp4)
- [十六向注视循环](../art/animation/v2/previews/final/look-loop.gif)
- [待机→跳跃→待机](../art/animation/v2/previews/final/idle-jump-idle.gif) / [有序关键帧](../art/animation/v2/previews/final/jump-transition-stills.png)
- [全部帧总览](../art/animation/v2/qa/contact-final.png) / [有标签视线对照](../art/animation/v2/qa/direction-labeled.png)
- [离线逐帧预览](../preview.html)：下载仓库或安装包后打开。浏览器渲染本轮未实测。

预览均解码最终无损 WEBP 生成；[预览来源记录](../art/animation/v2/previews/final/preview-manifest.json)绑定同一 SHA256。九状态依次为待机、右行、左行、挥手、跳跃、失败、等待、工作、检查。GIF／视频的时长不代表宿主的真实播放速度。

## 选稿与配准

使用者明确选择的注视第二行是 [第一组源图](../art/animation/v2/decoded/look-row-10.png)。该文件与使用者2026-10-27重发的第一张附图逐像素一致。重绘的第二组第5、6格侧脸和颈部变形，已弃用，不进入成品。

原始源图保持不动。以绿色优势通道规则清理原图背景，避免仅按纯绿 RGB 距离留下发束／翼尾间的暗绿。标准动作通过官方拆帧、检查及组装；额外几何配准每行动画只使用一套固定缩放与落地基线，保留跳跃的垂直位移。

注视第二行原始绘制尺寸略大，整张源画布统一缩放至第一行的共同尺度，八个姿势及间距使用同一矩阵；随后继续使用第一行登记的官方配准参数组装。没有逐格拉伸、独立缩放或重画五官。参见 [源图配准](../art/animation/v2/qa/look-source-registration.json)。成品从未经过重复边缘去色；每次重建均从原图重新处理，并在全部行组装后只做一次边缘去色。

## 已验证

最终图集：1536×2288、8×11、单格192×208，57个动作帧＋16个注视格＝73个有效格，其余15格全透明。

SHA256：`87e703010439e620479566b674a1bafa84542fd6f92387faf791600709d08111`。

| 检查 | 实际结果与证据 |
| --- | --- |
| 官方结构、透明度及色边检查 | 通过，[atlas-validation.json](../art/animation/v2/qa/atlas-validation.json) |
| 官方标准帧检查 | 九状态通过，无错误或警告，[review-final.json](../art/animation/v2/qa/review-final.json) |
| 三份隔离盲审与多数表决 | 四个主方向全部通过；112.5度的下视分量偏弱，[blind-validation.json](../art/animation/v2/qa/blind-validation.json) |
| 官方综合质量门槛 | 通过，跳跃峰值离地23px、落点与待机相差0px，注视横向中心最大漂移1px，[pet-quality.json](../art/animation/v2/qa/pet-quality.json) |
| 独立逐帧视觉复核 | 全73格从最终字节在原生浅／深背景下检查，无剩余硬缺陷，[视觉报告](../art/animation/v2/qa/final-independent-review.md) |
| Pets MCP 预检 | 同一最终WEBP返回 valid=true，[预检原始结果](../art/animation/v2/qa/mcp-preflight.json)；没有创建、更新或激活账号宠物 |

## 仍需审看的细节

112.5度接近水平向右，向下的幅度较弱；个别中间角度差异细微。337.5→000的像素差被连续性工具标为局部异常，复核后未见腰髋／脚底跳变，主要来自侧脸回正与抬头。保留这些警告，没有降低验证阈值。

浅紫与白色的复杂长发、蕾丝和手指在原生尺寸会损失细节；放大后仍能找到少量暗灰绿色／半透明亚像素色偏，不声称绝对零绿或完美边缘。此前原生尺寸可见的成片亮绿和两行身体比例阶差已修复。

本轮交付本地源码、素材与候选安装包。个人安装、账号云端活动宠物尚未更新；真实桌面的九状态触发、鼠标绕行一圈及资源刷新仍需实机验收。没有发布 Release 或推送远程 CI。

工程复跑11项隔离端到端测试全部通过，包括换装、备份恢复、异常回滚、Windows入口、ZIP解压安装与重复构建一致性。安装包只包含运行与维护文件；上方原图、动画审看素材及详细QA位于源码仓库，不随ZIP重复分发。
