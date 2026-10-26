# 换装实现

同一个 `gpt-chan` 身份对应一套当前安装图集；每套服装提供完整九种动作及十六向视线。服装不是可单独覆盖到所有姿势上的透明贴片。暂不增加安静版／表现版。

`outfits.json` 记录服装 ID、名称、相对目录及两项素材哈希。当前仅有已经完成的 `classic` 经典礼服。形象样稿不属于完整服装包，不列入可安装目录。

## 登记一套完成的服装

准备一个目录，包含 id=gpt-chan、spriteVersionNumber=2 的 pet.json、1536×2288 spritesheet.webp 和这套衍生素材的 NOTICE.md。不要改变角色 ID；署名与来源说明应随服装保留。

```text
python -m pip install -r requirements.txt
python scripts/petctl.py import-outfit winter-dress --source PATH_TO_COMPLETE_PACK --name "冬日礼服"
python scripts/build.py --no-previews
python scripts/petctl.py install --outfit winter-dress
python scripts/petctl.py install --outfit classic
```

冬日礼服是命令示例，不是现有成品。登记时会完整解码检查图集并复制至 outfits/winter-dress，之后自动出现在 catalog、发布包和预览器中。同名登记被拒绝，修订版使用新 ID。登记后还需按 [形象与动作验收](ART-DIRECTION.md) 做视觉检查。

切换复用安装事务：预校验、备份、替换、记录服装 ID；恢复上个服装用 backups／restore。宿主可能需要重新加载本地资源。仓库不保证热切换，也不会自动更新当前云端宠物。未来如增加云端切换，需接入宿主实际支持的 API，并继续保留原有云端 ID。
