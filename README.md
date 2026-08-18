# Shopify 开发工具箱

由 Young boy 维护的 Codex 插件，面向 Shopify Online Store 2.0 与跨境电商主题开发。

插件包含 19 个 Skill，覆盖功能迁移、代码修改保护、Schema、多语言、SEO、Markets、App 依赖、性能预算、Development Theme 预览、回归测试、Bug 定位、草稿主题同步、主题升级合并、无障碍、数据契约、交付报告、Git 工作流和 Theme Editor 使用说明。

## 安全边界

- 永久禁止发布 Shopify 主题。
- 禁止修改或上传到当前已发布主题。
- 远程写入只允许经过验证的 Development Theme 或未发布主题。
- 更新已有未发布主题前，必须验证数字 Theme ID、主题角色及文件清单。
- 默认先分析；只有用户明确要求修改时才改动本地文件。

## 安装

1. 克隆本仓库。
2. 将仓库根目录添加为本地 Codex 插件市场。
3. 从 `young-boy-shopify` 市场安装 `shopify-dev-toolkit`。
4. 新建 Codex 任务，使插件中的 Skill 生效。

命令行示例：

```powershell
codex plugin marketplace add <克隆后的仓库绝对路径>
codex plugin add shopify-dev-toolkit@young-boy-shopify
```

也可以在 Codex 插件界面选择对应的本地市场与插件。

## 使用示例

通常直接用自然语言描述任务即可：

```text
检查这个本地 Shopify 主题的 Schema、多语言和 SEO 问题，只分析，不修改。
```

```text
把源主题的购物车抽屉功能安全迁移到目标主题，先列出依赖和风险。
```

```text
把本地主题启动为 Development Theme，让我实时预览，禁止发布。
```

需要强制指定工作流时，可以输入 `$` 并选择相应的 Shopify Skill。

## 环境要求

- Codex 桌面应用或支持插件的 Codex 环境
- Python 3（运行部分静态检查脚本）
- Shopify CLI（仅在下载、预览或同步未发布主题时需要）
- 已获授权的 Shopify 店铺账号（仅在操作相应店铺时需要）

插件本身不保存 Shopify Token、登录 Cookie、店铺域名或 Theme ID。

## 使用许可

本项目不是开源软件。仓库公开仅用于查看、下载、安装和运行插件。未经版权所有者书面许可，不得修改、再发布、出售、制作衍生版本或将代码合并到其他项目。具体条款见 [LICENSE](LICENSE)。
