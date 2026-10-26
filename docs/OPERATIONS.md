# 安装、诊断与恢复

所有命令从仓库根目录或解压后的 Release 运行，需要 Python 3.10+。Windows 可以把 `python` 换成实际 Python 可执行文件；`install.ps1 -Python C:\path\python.exe` 可显式指定。macOS 可通过 GPTCHAN_PYTHON 指定解释器。

## 常用命令

```text
python scripts/petctl.py outfits
python scripts/petctl.py install --outfit classic
python scripts/petctl.py doctor
python scripts/petctl.py backups
python scripts/petctl.py restore BACKUP_ID
python scripts/petctl.py uninstall
```

安装、诊断、备份、恢复、卸载均接受 `--codex-home PATH`，优先于环境变量。doctor 和 backups 只读。卸载会把当前整个包移入备份，保留恢复机会；不删除其他宠物。

备份在 `CODEX_HOME/.pet-backups/gpt-chan/BACKUP_ID/`。恢复时填写 backups 输出的精确 ID；恢复前也备份当前包。已有损坏包会在安装替换前保留，但恢复命令会拒绝将不合法的配置重新安装；此类备份可人工检查。

旧版脚本创建的 `pets/gpt-chan.backup.*/original` 不会被自动迁移、删除或列作新式备份。需要恢复时先人工检查其中两个素材文件，保留原目录，再按手动安装方式处理。

## 校验与恢复边界

安装前检查 JSON 字段、原生 v2 图集 RIFF/静态 WebP 头部、尺寸、alpha 能力及目录中的 SHA256。登记新服装和构建时使用 Pillow 完整解码，检查透明像素和每行的有效格。运行时不安装图像库。目录内哈希用于一致性检查，不是对下载来源的数字签名；下载 ZIP 仍应与发布的 SHA256SUMS 比较。

文件先写入同卷暂存目录，校验后把旧目录移到备份，再切入新目录。普通异常会恢复旧目录；两个目录重命名之间有很短的空窗，这不是操作系统级的整笔原子事务。操作中请关闭使用该本地包的应用。磁盘损坏、断电、强杀进程等不能保证自动回滚。

若发生中断：先确认没有安装进程运行。保留 `.pet-staging` 中残留文件、`.pet-backups` 和 `.gpt-chan.lock` 作排查；检查目标与备份，必要时移走遗留锁文件，再使用 restore 恢复。不要在安装进程仍运行时移除锁。程序拒绝管理子路径中的符号链接或 junction，避免覆盖重定向位置。

## 界面仍显示旧版本

1. 用 doctor 查看实际 CODEX_HOME、安装发行版本、服装 ID、素材哈希与完整性。
2. 重新打开应用并确认选择了哪个宠物。doctor 不能识别账号当前活动云端 ID，它会明确输出来源未确认。
3. 若显示来自账号云端宠物，应通过宿主支持的更新流程更新该已有宠物；保持稳定身份，不能把本地复制成功视为云端已刷新。
4. 不自动改 WSL／运行后端、不改账号设置、不创建重复云端宠物。

本仓库的发行版本保存在 VERSION 与安装记录 release-info.json。spriteVersionNumber=2 是图集格式版本，与发行版本分开。
