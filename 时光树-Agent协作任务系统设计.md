# 时光树 - Agent 协作任务系统

## 一、系统概述

### 1.1 设计目标

| 目标 | 说明 |
|------|------|
| 并行效率 | 多Agent同步工作，减少等待依赖 |
| 任务追踪 | 实时掌握任务进度和阻塞情况 |
| 依赖管理 | 自动解析任务依赖关系，智能调度 |
| 质量把控 | 代码Review环节确保输出质量 |

### 1.2 Agent团队配置

| Agent | 角色 | 职责边界 |
|-------|------|---------|
| `ui_ux_agent` | UI/UX设计师 | 设计稿、设计规范、组件库 |
| `db_agent` | 数据库设计师 | 数据模型、SQL、索引、ER图 |
| `uniapp_agent` | UniApp移动端工程师 | 移动端页面、组件、插件 |
| `nextjs_agent` | Next.js管理后台工程师 | 管理后台页面、API对接 |
| `backend_go_agent` | Go后端工程师 | Go服务API、业务逻辑 |
| `backend_python_agent` | Python AI工程师 | AI服务、模型调用、向量存储 |

---

## 二、任务定义规范

### 2.1 任务结构

```json
{
  "task_id": "TASK-001",
  "title": "用户认证模块开发",
  "type": "feature|bugfix|design|research",
  "priority": "P0|P1|P2|P3",
  "status": "pending|ready|in_progress|review|completed|blocked",
  "assignee": "backend_go_agent",
  "dependents": [],
  "blocked_by": [],
  "spec": {
    "description": "实现手机号+验证码登录",
    "requirements": [
      "支持手机号+验证码登录",
      "支持微信一键登录",
      "JWT Token颁发与刷新"
    ],
    "api_spec": {},
    "design_spec": {},
    "db_spec": {}
  },
  "sub_tasks": [],
  "time_estimate": "2d",
  "actual_time": null,
  "created_at": "2026-04-02T10:00:00Z",
  "started_at": null,
  "completed_at": null,
  "comments": []
}
```

### 2.2 任务类型

| 类型 | 说明 | 典型工时 |
|------|------|---------|
| `feature` | 新功能开发 | 3-10d |
| `bugfix` | Bug修复 | 0.5-2d |
| `design` | 设计任务 | 2-5d |
| `research` | 技术调研 | 1-3d |
| `integration` | 集成联调 | 1-5d |

### 2.3 优先级定义

| 优先级 | 说明 | 响应要求 |
|--------|------|---------|
| `P0` | 最高优先级，阻塞主线 | 立即处理 |
| `P1` | 高优先级 | 24h内启动 |
| `P2` | 中优先级 | 3天内启动 |
| `P3` | 低优先级 | 1周内启动 |

---

## 三、M1阶段完整任务池

### 3.1 UI/UX Agent 任务

```yaml
ui_ux_tasks:
  - task_id: "TASK-UI-001"
    title: "设计系统基础规范"
    type: "design"
    priority: "P0"
    assignee: "ui_ux_agent"
    time_estimate: "3d"
    blocked_by: []
    
  - task_id: "TASK-UI-002"
    title: "孕期插件UI设计稿"
    type: "design"
    priority: "P0"
    assignee: "ui_ux_agent"
    time_estimate: "5d"
    blocked_by: ["TASK-UI-001"]
    
  - task_id: "TASK-UI-003"
    title: "婴儿期插件UI设计稿"
    type: "design"
    priority: "P0"
    assignee: "ui_ux_agent"
    time_estimate: "5d"
    blocked_by: ["TASK-UI-001"]
    
  - task_id: "TASK-UI-004"
    title: "管理后台UI设计稿"
    type: "design"
    priority: "P1"
    assignee: "ui_ux_agent"
    time_estimate: "5d"
    blocked_by: ["TASK-UI-001"]
    
  - task_id: "TASK-UI-005"
    title: "年龄适配主题系统"
    type: "design"
    priority: "P1"
    assignee: "ui_ux_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-UI-002", "TASK-UI-003"]
```

### 3.2 Database Agent 任务

```yaml
db_tasks:
  - task_id: "TASK-DB-001"
    title: "核心数据模型设计"
    type: "design"
    priority: "P0"
    assignee: "db_agent"
    time_estimate: "3d"
    blocked_by: []
    spec:
      tables:
        - users
        - lives
        - families
        - family_members
        
  - task_id: "TASK-DB-002"
    title: "时间轴与内容表设计"
    type: "design"
    priority: "P0"
    assignee: "db_agent"
    time_estimate: "2d"
    blocked_by: ["TASK-DB-001"]
    spec:
      tables:
        - timeline
        - timeline_likes
        - timeline_comments
        - contents
        
  - task_id: "TASK-DB-003"
    title: "AI服务表设计"
    type: "design"
    priority: "P1"
    assignee: "db_agent"
    time_estimate: "2d"
    blocked_by: ["TASK-DB-001"]
    spec:
      tables:
        - ai_sessions
        - ai_messages
        - ai_analysis_results
        
  - task_id: "TASK-DB-004"
    title: "数据库索引优化设计"
    type: "design"
    priority: "P1"
    assignee: "db_agent"
    time_estimate: "1d"
    blocked_by: ["TASK-DB-002", "TASK-DB-003"]
    
  - task_id: "TASK-DB-005"
    title: "公私空间隔离实现"
    type: "design"
    priority: "P0"
    assignee: "db_agent"
    time_estimate: "2d"
    blocked_by: ["TASK-DB-001"]
```

### 3.3 UniApp Agent 任务

```yaml
uniapp_tasks:
  - task_id: "TASK-UNI-001"
    title: "UniApp项目脚手架搭建"
    type: "feature"
    priority: "P0"
    assignee: "uniapp_agent"
    time_estimate: "2d"
    blocked_by: []
    
  - task_id: "TASK-UNI-002"
    title: "底座框架开发（认证+生命周期）"
    type: "feature"
    priority: "P0"
    assignee: "uniapp_agent"
    time_estimate: "5d"
    blocked_by: ["TASK-UNI-001", "TASK-DB-001"]
    
  - task_id: "TASK-UNI-003"
    title: "公私空间切换组件"
    type: "feature"
    priority: "P0"
    assignee: "uniapp_agent"
    time_estimate: "2d"
    blocked_by: ["TASK-UNI-002", "TASK-DB-005"]
    
  - task_id: "TASK-UNI-004"
    title: "孕期插件UI开发"
    type: "feature"
    priority: "P0"
    assignee: "uniapp_agent"
    time_estimate: "5d"
    blocked_by: ["TASK-UNI-002", "TASK-UI-002"]
    
  - task_id: "TASK-UNI-005"
    title: "婴儿期插件UI开发"
    type: "feature"
    priority: "P0"
    assignee: "uniapp_agent"
    time_estimate: "5d"
    blocked_by: ["TASK-UNI-002", "TASK-UI-003"]
    
  - task_id: "TASK-UNI-006"
    title: "年龄适配主题集成"
    type: "feature"
    priority: "P1"
    assignee: "uniapp_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-UNI-004", "TASK-UNI-005", "TASK-UI-005"]
```

### 3.4 Next.js Agent 任务

```yaml
nextjs_tasks:
  - task_id: "TASK-Next-001"
    title: "Next.js项目脚手架搭建"
    type: "feature"
    priority: "P0"
    assignee: "nextjs_agent"
    time_estimate: "2d"
    blocked_by: []
    
  - task_id: "TASK-Next-002"
    title: "管理后台布局框架"
    type: "feature"
    priority: "P0"
    assignee: "nextjs_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-Next-001", "TASK-UI-001"]
    
  - task_id: "TASK-Next-003"
    title: "用户管理页面开发"
    type: "feature"
    priority: "P0"
    assignee: "nextjs_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-Next-002", "TASK-BE-GO-002"]
    
  - task_id: "TASK-Next-004"
    title: "家庭管理页面开发"
    type: "feature"
    priority: "P0"
    assignee: "nextjs_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-Next-002", "TASK-BE-GO-003"]
    
  - task_id: "TASK-Next-005"
    title: "数据分析看板开发"
    type: "feature"
    priority: "P1"
    assignee: "nextjs_agent"
    time_estimate: "4d"
    blocked_by: ["TASK-Next-002", "TASK-BE-GO-006"]
```

### 3.5 Go Backend Agent 任务

```yaml
go_tasks:
  - task_id: "TASK-BE-GO-001"
    title: "Go项目结构搭建"
    type: "feature"
    priority: "P0"
    assignee: "backend_go_agent"
    time_estimate: "1d"
    blocked_by: []
    
  - task_id: "TASK-BE-GO-002"
    title: "用户认证API开发"
    type: "feature"
    priority: "P0"
    assignee: "backend_go_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-BE-GO-001", "TASK-DB-001"]
    
  - task_id: "TASK-BE-GO-003"
    title: "生命管理API开发"
    type: "feature"
    priority: "P0"
    assignee: "backend_go_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-BE-GO-001", "TASK-DB-001"]
    
  - task_id: "TASK-BE-GO-004"
    title: "家庭管理API开发"
    type: "feature"
    priority: "P0"
    assignee: "backend_go_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-BE-GO-001", "TASK-DB-001", "TASK-DB-005"]
    
  - task_id: "TASK-BE-GO-005"
    title: "时间轴API开发"
    type: "feature"
    priority: "P0"
    assignee: "backend_go_agent"
    time_estimate: "4d"
    blocked_by: ["TASK-BE-GO-001", "TASK-DB-002"]
    
  - task_id: "TASK-BE-GO-006"
    title: "统计分析API开发"
    type: "feature"
    priority: "P1"
    assignee: "backend_go_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-BE-GO-001", "TASK-DB-004"]
```

### 3.6 Python AI Agent 任务

```yaml
python_tasks:
  - task_id: "TASK-BE-PY-001"
    title: "Python AI服务脚手架"
    type: "feature"
    priority: "P0"
    assignee: "backend_python_agent"
    time_estimate: "1d"
    blocked_by: []
    
  - task_id: "TASK-BE-PY-002"
    title: "向量数据库集成"
    type: "feature"
    priority: "P0"
    assignee: "backend_python_agent"
    time_estimate: "3d"
    blocked_by: ["TASK-BE-PY-001", "TASK-DB-003"]
    
  - task_id: "TASK-BE-PY-003"
    title: "长期记忆引擎开发"
    type: "feature"
    priority: "P0"
    assignee: "backend_python_agent"
    time_estimate: "5d"
    blocked_by: ["TASK-BE-PY-002"]
    
  - task_id: "TASK-BE-PY-004"
    title: "情感分析服务开发"
    type: "feature"
    priority: "P0"
    assignee: "backend_python_agent"
    time_estimate: "4d"
    blocked_by: ["TASK-BE-PY-001"]
    
  - task_id: "TASK-BE-PY-005"
    title: "AI对话服务开发"
    type: "feature"
    priority: "P1"
    assignee: "backend_python_agent"
    time_estimate: "4d"
    blocked_by: ["TASK-BE-PY-003"]
```

---

## 四、依赖关系图

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        M1 阶段任务依赖图                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  [UI-001] ──┬──► [UI-002] ──┐                                          │
│             │──► [UI-003] ──┼──► [UI-005]                              │
│             └──► [UI-004] ──┘                                          │
│                                                                          │
│  [DB-001] ──┬──► [DB-002] ──┬──► [DB-004]                              │
│             │──► [DB-003] ──┘                                          │
│             └──► [DB-005] ───────────────────────────────────────────┐  │
│                                                                       │  │
│  [GO-001] ──┬──► [GO-002] ──┐                                         │  │
│             │──► [GO-003] ──┤                                         │  │
│             │──► [GO-004] ──┼──► [GO-006]                             │  │
│             └──► [GO-005] ──┘                                         │  │
│                                                                       │  │
│  [PY-001] ──┬──► [PY-002] ──┬──► [PY-003] ──► [PY-005]              │  │
│             └──► [PY-004] ──┘                                         │  │
│                                                                       │  │
│  [UNI-001] ─┼──► [UNI-002] ─┼──► [UNI-003]                          │  │
│             │──► [UNI-004] ─┤                                         │  │
│             └──► [UNI-005] ─┴──► [UNI-006]                          │  │
│                                                                       │  │
│  [NEXT-001]─┼──► [NEXT-002]─┼──► [NEXT-003]                          │  │
│             │──► [NEXT-004]─┤                                         │  │
│             └──► [NEXT-005]─┘                                         │  │
│                                                                       │  │
│  跨Agent依赖：                                                         │  │
│  [DB-001] ──────────────────► [UNI-002], [GO-002], [GO-003]          │  │
│  [DB-002] ──────────────────► [GO-005]                               │  │
│  [DB-005] ──────────────────► [UNI-003], [GO-004]                    │  │
│  [UI-002]  ─────────────────► [UNI-004]                               │  │
│  [UI-003]  ─────────────────► [UNI-005]                               │  │
│  [UI-005]  ─────────────────► [UNI-006]                               │  │
│  [UI-001]  ─────────────────► [NEXT-002]                              │  │
│  [GO-002]  ─────────────────► [NEXT-003]                              │  │
│  [GO-003]  ─────────────────► [NEXT-004]                              │  │
│  [GO-006]  ─────────────────► [NEXT-005]                              │  │
│  [PY-003]  ─────────────────► [UNI-006] (AI能力)                      │  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 五、并行调度算法

### 5.1 调度规则

```python
def can_start_task(task, completed_tasks, in_progress_tasks):
    """
    判断任务是否可以启动
    """
    # 1. 检查阻塞任务是否完成
    for blocked_by in task.blocked_by:
        if blocked_by not in completed_tasks:
            return False, f"Blocked by {blocked_by}"
    
    # 2. 检查是否有相同 assignee 的任务在进行中
    for in_progress in in_progress_tasks:
        if in_progress.assignee == task.assignee:
            return False, f"Agent {task.assignee} is busy with {in_progress.task_id}"
    
    # 3. 检查资源限制
    if len([t for t in in_progress_tasks if t.assignee == task.assignee]) >= MAX_TASKS_PER_AGENT:
        return False, f"Agent {task.assignee} has too many tasks"
    
    return True, "Ready to start"

def schedule_tasks(all_tasks):
    """
    调度算法：尽可能最大化并行度
    """
    completed = []
    in_progress = []
    ready_queue = []
    
    # 按优先级排序
    sorted_tasks = sort_by_priority(all_tasks)
    
    for task in sorted_tasks:
        can_start, reason = can_start_task(task, completed, in_progress)
        
        if can_start:
            task.status = "ready"
            ready_queue.append(task)
        else:
            task.status = "pending"
            task.blocked_reason = reason
    
    return ready_queue, pending_tasks
```

### 5.2 Agent工作负载均衡

| Agent | 最大并行任务数 | 当前任务数 | 负载率 |
|-------|---------------|-----------|--------|
| `ui_ux_agent` | 2 | 1 | 50% |
| `db_agent` | 2 | 1 | 50% |
| `uniapp_agent` | 3 | 2 | 67% |
| `nextjs_agent` | 3 | 1 | 33% |
| `backend_go_agent` | 3 | 2 | 67% |
| `backend_python_agent` | 2 | 1 | 50% |

---

## 六、任务状态流转

### 6.1 状态机

```
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    ▼                                         │
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┴───┐
  │ pending  │───►│  ready   │───►│in_progress│───►│   review    │
  └──────────┘    └──────────┘    └──────────┘    └─────────────┘
       │               │               │                  │
       │               │               │                  │
       │               │               ▼                  ▼
       │               │          ┌─────────┐      ┌──────────┐
       │               │          │ blocked │      │completed │
       │               │          └─────────┘      └──────────┘
       │               │               │
       │               │               │
       └───────────────┴───────────────┴────────────
                        (unblock)
```

### 6.2 状态转换规则

| 当前状态 | 事件 | 下一状态 | 触发条件 |
|---------|------|---------|---------|
| `pending` | 阻塞解除 | `ready` | 所有 blocked_by 完成 |
| `ready` | Agent认领 | `in_progress` | Agent开始处理 |
| `in_progress` | 完成开发 | `review` | 提交Code Review |
| `review` | Review通过 | `completed` | PR合并 |
| `review` | Review拒绝 | `in_progress` | 需修复问题 |
| `in_progress` | 发现阻塞 | `blocked` | 依赖未满足 |
| `blocked` | 阻塞解除 | `in_progress` | 重新开始 |

---

## 七、Agent通信协议

### 7.1 任务完成通知

```json
{
  "type": "TASK_COMPLETED",
  "task_id": "TASK-DB-001",
  "assignee": "db_agent",
  "completed_at": "2026-04-05T18:00:00Z",
  "outputs": [
    {
      "type": "sql_file",
      "path": "/schema/core_tables.sql",
      "description": "核心表建表SQL"
    },
    {
      "type": "er_diagram",
      "path": "/docs/er_core.svg",
      "description": "核心实体关系图"
    }
  ],
  "notify_agents": ["uniapp_agent", "backend_go_agent"]
}
```

### 7.2 任务阻塞通知

```json
{
  "type": "TASK_BLOCKED",
  "task_id": "TASK-UNI-004",
  "blocked_by": "TASK-DB-001",
  "reason": "等待数据库表设计完成",
  "expected_completion": "2026-04-05T18:00:00Z"
}
```

### 7.3 任务依赖请求

```json
{
  "type": "DEPENDENCY_REQUEST",
  "from_task": "TASK-UNI-004",
  "from_agent": "uniapp_agent",
  "requested_dependency": "TASK-DB-001",
  "needed_outputs": ["建表SQL", "ER图", "API设计文档"],
  "urgency": "high"
}
```

---

## 八、Code Review 流程

### 8.1 Review 规则

| 任务类型 | 必须 Review | Reviewer |
|---------|------------|----------|
| `feature` | 是 | 2人（1同组+1跨组） |
| `bugfix` | 是 | 1人（同组） |
| `design` | 是 | 1人（设计专家） |
| `integration` | 是 | 2人（各1端） |

### 8.2 Review 检查清单

```markdown
## Code Review Checklist

### 功能性
- [ ] 代码实现了需求文档中的所有功能点
- [ ] 边界条件和异常情况已处理
- [ ] 单元测试覆盖率 > 80%

### 代码质量
- [ ] 遵循项目编码规范
- [ ] 无硬编码配置
- [ ] 无安全漏洞（SQL注入、XSS等）
- [ ] 注释完整，复杂逻辑有说明

### 性能
- [ ] 数据库查询有索引
- [ ] 无N+1查询问题
- [ ] 敏感操作有防抖/节流

### 集成
- [ ] API格式符合规范
- [ ] 前后端数据模型一致
- [ ] 文档已更新
```

---

## 九、任务板视图

### 9.1 M1 阶段 Sprint 看板

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 时光树 M1 阶段 Sprint 看板                              2026-Q1 │ 总任务: 26 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  TODO (6)              IN PROGRESS (5)        REVIEW (2)      DONE (13)       │
│  ┌─────────────┐     ┌─────────────┐      ┌─────────────┐  ┌─────────────┐│
│  │ TASK-UI-005 │     │ TASK-UI-001 │      │ TASK-DB-002 │  │ TASK-GO-001 ││
│  │ UI: 3d      │     │ UI: 3d      │      │ DB: 2d      │  │ GO: 1d      ││
│  │ blocked     │     │ 50%         │      │ Reviewing   │  │ completed   ││
│  └─────────────┘     └─────────────┘      └─────────────┘  └─────────────┘│
│  ┌─────────────┐     ┌─────────────┐      ┌─────────────┐  ┌─────────────┐│
│  │ TASK-NEXT-005│    │ TASK-DB-001 │      │ TASK-UNI-003│  │ TASK-PY-001 ││
│  │ Next: 4d    │     │ DB: 3d      │      │ UNI: 2d     │  │ PY: 1d      ││
│  │ blocked     │     │ 70%         │      │ 80%         │  │ completed   ││
│  └─────────────┘     └─────────────┘      └─────────────┘  └─────────────┘│
│  ┌─────────────┐     ┌─────────────┐                       ┌─────────────┐│
│  │ TASK-BE-PY-005│    │ TASK-GO-002 │                       │ TASK-UNI-001││
│  │ PY: 4d       │     │ GO: 3d      │                       │ UNI: 2d     ││
│  │ blocked      │     │ 40%         │                       │ completed   ││
│  └─────────────┘     └─────────────┘                       └─────────────┘│
│  ┌─────────────┐     ┌─────────────┐                       ┌─────────────┐│
│  │             │     │ TASK-UNI-002│                       │ TASK-DB-003 ││
│  │             │     │ UNI: 5d      │                       │ DB: 2d      ││
│  │             │     │ 30%         │                       │ completed   ││
│  │             │     └─────────────┘                       └─────────────┘│
│  │             │     ┌─────────────┐                       ┌─────────────┐│
│  │             │     │ TASK-PY-002 │                       │ TASK-BE-GO-001│
│  │             │     │ PY: 3d      │                       │ GO: 1d      ││
│  │             │     │ 20%         │                       │ completed   ││
│  └─────────────┘     └─────────────┘                       └─────────────┘│
│                                                                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ blocked tasks: 3                                                            │
│ 团队负载: UI(50%) DB(50%) UNI(67%) NEXT(33%) GO(67%) PY(50%)               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 十、每日站会输出

### 10.1 站会模板

```markdown
# 时光树 M1 Sprint 每日站会
## 日期: 2026-04-03

### 各Agent进度

#### UI/UX Agent
- 昨日完成: TASK-UI-001 设计系统基础规范 70%
- 今日计划: 完成设计系统基础规范，开始孕期设计稿
- 阻塞: 无

#### Database Agent  
- 昨日完成: TASK-DB-001 核心数据模型设计 70%
- 今日计划: 完成核心表设计，输出SQL和ER图
- 阻塞: 无

#### UniApp Agent
- 昨日完成: TASK-UNI-001 项目脚手架搭建 100%
- 今日计划: 开始 TASK-UNI-002 底座框架开发
- 阻塞: 等待 TASK-DB-001 完成以获取表结构

#### Next.js Agent
- 昨日完成: TASK-NEXT-001 项目脚手架搭建 100%
- 今日计划: 开始 TASK-NEXT-002 管理后台布局框架
- 阻塞: 等待 UI-001 设计系统规范

#### Go Backend Agent
- 昨日完成: TASK-BE-GO-001 项目结构搭建 100%
- 今日计划: 开始 TASK-BE-GO-002 用户认证API
- 阻塞: 无

#### Python AI Agent
- 昨日完成: TASK-BE-PY-001 AI服务脚手架 100%
- 今日计划: 开始 TASK-BE-PY-002 向量数据库集成
- 阻塞: 无

### 依赖关系更新
- [更新] TASK-UNI-002 阻塞于 TASK-DB-001（预计 2026-04-04 完成）

### 风险提示
- [风险] UI-005 依赖于 UI-002 和 UI-003，可能影响 UNI-006 进度

### 明日计划
- 继续并行开发，重点推进 DB-001, GO-002, UNI-002
```

---

## 十一、实施工具建议

### 11.1 推荐工具链

| 工具 | 用途 | 说明 |
|------|------|------|
| Linear | 任务管理 | 支持依赖管理、状态流转 |
| GitHub Projects | 任务看板 | 与代码仓库集成 |
| Notion | 文档管理 | 团队知识库 |
| Slack/飞书 | 通信 | Agent间通知 |
| GitHub PR | Code Review | 内置Review流程 |
| Jenkins/GitHub Actions | CI/CD | 自动化构建测试 |

### 11.2 集成架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Agent协作任务系统                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ Linear   │◄──►│ GitHub   │◄──►│  CI/CD   │                  │
│  │ 任务管理  │    │ PR/代码   │    │ 构建测试  │                  │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘                  │
│       │               │               │                          │
│       │         ┌─────┴─────┐         │                          │
│       │         │  通知系统  │◄────────┘                          │
│       │         └─────┬─────┘                                    │
│       │               │                                          │
│       │         ┌─────┴─────┐                                    │
│       └────────►│  Dashboard │                                    │
│                 └───────────┘                                    │
└─────────────────────────────────────────────────────────────────┘
```
