#!/usr/bin/env python3
"""
时光树 - Agent 协作任务执行系统
实现多Agent并行工作、任务调度、依赖管理
"""

import json
import uuid
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field, asdict
from collections import defaultdict


class TaskStatus(Enum):
    PENDING = "pending"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class TaskPriority(Enum):
    P0 = "P0"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"


class TaskType(Enum):
    FEATURE = "feature"
    BUGFIX = "bugfix"
    DESIGN = "design"
    RESEARCH = "research"
    INTEGRATION = "integration"


@dataclass
class TaskOutput:
    type: str
    path: str
    description: str


@dataclass
class TaskSpec:
    description: str
    requirements: List[str] = field(default_factory=list)
    api_spec: Dict = field(default_factory=dict)
    design_spec: Dict = field(default_factory=dict)
    db_spec: Dict = field(default_factory=dict)
    tables: List[str] = field(default_factory=list)


@dataclass
class Task:
    task_id: str
    title: str
    task_type: str
    priority: str
    status: str
    assignee: str
    blocked_by: List[str] = field(default_factory=list)
    spec: TaskSpec = field(default_factory=TaskSpec)
    sub_tasks: List[str] = field(default_factory=list)
    time_estimate: str = ""
    actual_time: Optional[str] = None
    created_at: str = ""
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    outputs: List[TaskOutput] = field(default_factory=list)
    blocked_reason: str = ""
    sprint: str = "M1"
    
    def to_dict(self):
        return {
            "task_id": self.task_id,
            "title": self.title,
            "type": self.task_type,
            "priority": self.priority,
            "status": self.status,
            "assignee": self.assignee,
            "blocked_by": self.blocked_by,
            "spec": asdict(self.spec),
            "time_estimate": self.time_estimate,
            "actual_time": self.actual_time,
            "created_at": self.created_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "outputs": [asdict(o) for o in self.outputs],
            "blocked_reason": self.blocked_reason,
            "sprint": self.sprint
        }


class Agent:
    def __init__(self, agent_id: str, name: str, max_parallel: int = 2):
        self.agent_id = agent_id
        self.name = name
        self.max_parallel = max_parallel
        self.current_tasks: List[str] = []
        self.completed_tasks: List[str] = []
        self.capabilities: List[str] = []
        
    def can_accept_task(self) -> bool:
        return len(self.current_tasks) < self.max_parallel
    
    def assign_task(self, task_id: str):
        self.current_tasks.append(task_id)
        
    def complete_task(self, task_id: str):
        if task_id in self.current_tasks:
            self.current_tasks.remove(task_id)
        self.completed_tasks.append(task_id)
    
    @property
    def workload(self) -> float:
        return len(self.current_tasks) / self.max_parallel


class AgentCollaborationSystem:
    """Agent协作任务执行系统"""
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.agents: Dict[str, Agent] = {}
        self.task_history: List[Dict] = []
        
        self._init_agents()
        self._init_m1_tasks()
    
    def _init_agents(self):
        """初始化Agent团队"""
        agent_configs = [
            ("ui_ux_agent", "UI/UX设计师", 2),
            ("db_agent", "数据库设计师", 2),
            ("uniapp_agent", "UniApp移动端工程师", 3),
            ("nextjs_agent", "Next.js管理后台工程师", 3),
            ("backend_go_agent", "Go后端工程师", 3),
            ("backend_python_agent", "Python AI工程师", 2),
        ]
        
        for agent_id, name, max_parallel in agent_configs:
            self.agents[agent_id] = Agent(agent_id, name, max_parallel)
    
    def _init_m1_tasks(self):
        """初始化M1阶段任务池"""
        m1_tasks = [
            # UI/UX Tasks
            Task(
                task_id="TASK-UI-001", title="设计系统基础规范", task_type="design",
                priority="P0", status="pending", assignee="ui_ux_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                spec=TaskSpec(description="建立时光树设计系统基础规范，包括色彩、字体、间距、圆角等")
            ),
            Task(
                task_id="TASK-UI-002", title="孕期插件UI设计稿", task_type="design",
                priority="P0", status="pending", assignee="ui_ux_agent",
                time_estimate="5d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UI-001"],
                spec=TaskSpec(description="孕期插件完整UI设计稿")
            ),
            Task(
                task_id="TASK-UI-003", title="婴儿期插件UI设计稿", task_type="design",
                priority="P0", status="pending", assignee="ui_ux_agent",
                time_estimate="5d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UI-001"],
                spec=TaskSpec(description="婴儿期插件完整UI设计稿")
            ),
            Task(
                task_id="TASK-UI-004", title="管理后台UI设计稿", task_type="design",
                priority="P1", status="pending", assignee="ui_ux_agent",
                time_estimate="5d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UI-001"],
                spec=TaskSpec(description="管理后台完整UI设计稿")
            ),
            Task(
                task_id="TASK-UI-005", title="年龄适配主题系统", task_type="design",
                priority="P1", status="pending", assignee="ui_ux_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UI-002", "TASK-UI-003"],
                spec=TaskSpec(description="7个年龄段的UI适配主题系统")
            ),
            
            # Database Tasks
            Task(
                task_id="TASK-DB-001", title="核心数据模型设计", task_type="design",
                priority="P0", status="pending", assignee="db_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                spec=TaskSpec(
                    description="核心数据模型设计",
                    tables=["users", "lives", "families", "family_members"]
                )
            ),
            Task(
                task_id="TASK-DB-002", title="时间轴与内容表设计", task_type="design",
                priority="P0", status="pending", assignee="db_agent",
                time_estimate="2d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-DB-001"],
                spec=TaskSpec(
                    description="时间轴与内容管理表设计",
                    tables=["timeline", "timeline_likes", "timeline_comments", "contents"]
                )
            ),
            Task(
                task_id="TASK-DB-003", title="AI服务表设计", task_type="design",
                priority="P1", status="pending", assignee="db_agent",
                time_estimate="2d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-DB-001"],
                spec=TaskSpec(
                    description="AI服务相关表设计",
                    tables=["ai_sessions", "ai_messages", "ai_analysis_results"]
                )
            ),
            Task(
                task_id="TASK-DB-004", title="数据库索引优化设计", task_type="design",
                priority="P1", status="pending", assignee="db_agent",
                time_estimate="1d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-DB-002", "TASK-DB-003"],
                spec=TaskSpec(description="数据库索引优化设计文档")
            ),
            Task(
                task_id="TASK-DB-005", title="公私空间隔离实现", task_type="design",
                priority="P0", status="pending", assignee="db_agent",
                time_estimate="2d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-DB-001"],
                spec=TaskSpec(description="公私空间隔离数据库层实现方案")
            ),
            
            # UniApp Tasks
            Task(
                task_id="TASK-UNI-001", title="UniApp项目脚手架搭建", task_type="feature",
                priority="P0", status="pending", assignee="uniapp_agent",
                time_estimate="2d", created_at=datetime.now().isoformat(),
                spec=TaskSpec(description="UniApp项目创建、配置Vue3、Pinia、路由等基础框架")
            ),
            Task(
                task_id="TASK-UNI-002", title="底座框架开发", task_type="feature",
                priority="P0", status="pending", assignee="uniapp_agent",
                time_estimate="5d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UNI-001", "TASK-DB-001"],
                spec=TaskSpec(description="用户认证、生命周期管理、公私空间切换等底座功能")
            ),
            Task(
                task_id="TASK-UNI-003", title="公私空间切换组件", task_type="feature",
                priority="P0", status="pending", assignee="uniapp_agent",
                time_estimate="2d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UNI-002", "TASK-DB-005"],
                spec=TaskSpec(description="公私空间可视化切换组件")
            ),
            Task(
                task_id="TASK-UNI-004", title="孕期插件UI开发", task_type="feature",
                priority="P0", status="pending", assignee="uniapp_agent",
                time_estimate="5d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UNI-002", "TASK-UI-002"],
                spec=TaskSpec(description="孕期插件页面开发")
            ),
            Task(
                task_id="TASK-UNI-005", title="婴儿期插件UI开发", task_type="feature",
                priority="P0", status="pending", assignee="uniapp_agent",
                time_estimate="5d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UNI-002", "TASK-UI-003"],
                spec=TaskSpec(description="婴儿期插件页面开发")
            ),
            Task(
                task_id="TASK-UNI-006", title="年龄适配主题集成", task_type="feature",
                priority="P1", status="pending", assignee="uniapp_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-UNI-004", "TASK-UNI-005", "TASK-UI-005"],
                spec=TaskSpec(description="年龄适配主题在移动端的集成")
            ),
            
            # Next.js Tasks
            Task(
                task_id="TASK-NEXT-001", title="Next.js项目脚手架搭建", task_type="feature",
                priority="P0", status="pending", assignee="nextjs_agent",
                time_estimate="2d", created_at=datetime.now().isoformat(),
                spec=TaskSpec(description="Next.js 14项目创建、配置TypeScript、Tailwind等")
            ),
            Task(
                task_id="TASK-NEXT-002", title="管理后台布局框架", task_type="feature",
                priority="P0", status="pending", assignee="nextjs_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-NEXT-001", "TASK-UI-001"],
                spec=TaskSpec(description="管理后台整体布局框架")
            ),
            Task(
                task_id="TASK-NEXT-003", title="用户管理页面开发", task_type="feature",
                priority="P0", status="pending", assignee="nextjs_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-NEXT-002", "TASK-BE-GO-002"],
                spec=TaskSpec(description="用户列表、用户详情、状态管理页面")
            ),
            Task(
                task_id="TASK-NEXT-004", title="家庭管理页面开发", task_type="feature",
                priority="P0", status="pending", assignee="nextjs_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-NEXT-002", "TASK-BE-GO-003"],
                spec=TaskSpec(description="家庭列表、家庭详情、成员管理页面")
            ),
            Task(
                task_id="TASK-NEXT-005", title="数据分析看板开发", task_type="feature",
                priority="P1", status="pending", assignee="nextjs_agent",
                time_estimate="4d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-NEXT-002", "TASK-BE-GO-006"],
                spec=TaskSpec(description="DAU/MAU统计、内容贡献等数据看板")
            ),
            
            # Go Backend Tasks
            Task(
                task_id="TASK-BE-GO-001", title="Go项目结构搭建", task_type="feature",
                priority="P0", status="pending", assignee="backend_go_agent",
                time_estimate="1d", created_at=datetime.now().isoformat(),
                spec=TaskSpec(description="Go项目目录结构、中间件、项目规范")
            ),
            Task(
                task_id="TASK-BE-GO-002", title="用户认证API开发", task_type="feature",
                priority="P0", status="pending", assignee="backend_go_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-GO-001", "TASK-DB-001"],
                spec=TaskSpec(description="手机号登录、微信登录、JWT Token API")
            ),
            Task(
                task_id="TASK-BE-GO-003", title="生命管理API开发", task_type="feature",
                priority="P0", status="pending", assignee="backend_go_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-GO-001", "TASK-DB-001"],
                spec=TaskSpec(description="Life ID管理、阶段切换API")
            ),
            Task(
                task_id="TASK-BE-GO-004", title="家庭管理API开发", task_type="feature",
                priority="P0", status="pending", assignee="backend_go_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-GO-001", "TASK-DB-001", "TASK-DB-005"],
                spec=TaskSpec(description="创建/加入家庭、成员管理API")
            ),
            Task(
                task_id="TASK-BE-GO-005", title="时间轴API开发", task_type="feature",
                priority="P0", status="pending", assignee="backend_go_agent",
                time_estimate="4d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-GO-001", "TASK-DB-002"],
                spec=TaskSpec(description="时间轴CRUD、点赞评论API")
            ),
            Task(
                task_id="TASK-BE-GO-006", title="统计分析API开发", task_type="feature",
                priority="P1", status="pending", assignee="backend_go_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-GO-001", "TASK-DB-004"],
                spec=TaskSpec(description="DAU/MAU、内容统计API")
            ),
            
            # Python AI Tasks
            Task(
                task_id="TASK-BE-PY-001", title="Python AI服务脚手架", task_type="feature",
                priority="P0", status="pending", assignee="backend_python_agent",
                time_estimate="1d", created_at=datetime.now().isoformat(),
                spec=TaskSpec(description="Python AI服务目录结构、FastAPI框架、依赖")
            ),
            Task(
                task_id="TASK-BE-PY-002", title="向量数据库集成", task_type="feature",
                priority="P0", status="pending", assignee="backend_python_agent",
                time_estimate="3d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-PY-001", "TASK-DB-003"],
                spec=TaskSpec(description="Milvus/Qdrant向量数据库集成")
            ),
            Task(
                task_id="TASK-BE-PY-003", title="长期记忆引擎开发", task_type="feature",
                priority="P0", status="pending", assignee="backend_python_agent",
                time_estimate="5d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-PY-002"],
                spec=TaskSpec(description="AI长期记忆存储与检索引擎")
            ),
            Task(
                task_id="TASK-BE-PY-004", title="情感分析服务开发", task_type="feature",
                priority="P0", status="pending", assignee="backend_python_agent",
                time_estimate="4d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-PY-001"],
                spec=TaskSpec(description="文本情感分析服务开发")
            ),
            Task(
                task_id="TASK-BE-PY-005", title="AI对话服务开发", task_type="feature",
                priority="P1", status="pending", assignee="backend_python_agent",
                time_estimate="4d", created_at=datetime.now().isoformat(),
                blocked_by=["TASK-BE-PY-003"],
                spec=TaskSpec(description="家庭AI、个人AI对话服务")
            ),
        ]
        
        for task in m1_tasks:
            self.tasks[task.task_id] = task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)
    
    def get_completed_tasks(self) -> List[str]:
        return [t.task_id for t in self.tasks.values() if t.status == TaskStatus.COMPLETED.value]
    
    def get_in_progress_tasks(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.status == TaskStatus.IN_PROGRESS.value]
    
    def get_ready_tasks(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.status == TaskStatus.READY.value]
    
    def get_blocked_tasks(self) -> List[Task]:
        return [t for t in self.tasks.values() if t.status == TaskStatus.BLOCKED.value]
    
    def _check_can_start(self, task: Task) -> tuple[bool, str]:
        """检查任务是否可以启动"""
        completed = self.get_completed_tasks()
        in_progress = self.get_in_progress_tasks()
        
        for blocked_by in task.blocked_by:
            if blocked_by not in completed:
                blocker = self.get_task(blocked_by)
                blocker_status = blocker.status if blocker else "unknown"
                return False, f"Blocked by {blocked_by} ({blocker_status})"
        
        agent = self.agents.get(task.assignee)
        if not agent:
            return False, f"Unknown agent: {task.assignee}"
        
        if not agent.can_accept_task():
            busy_tasks = [t.task_id for t in in_progress if t.assignee == task.assignee]
            return False, f"Agent {task.assignee} busy with {busy_tasks}"
        
        return True, "Ready"
    
    def _evaluate_ready_tasks(self):
        """评估并更新所有任务的状态"""
        completed = set(self.get_completed_tasks())
        
        for task in self.tasks.values():
            if task.status in [TaskStatus.COMPLETED.value, TaskStatus.IN_PROGRESS.value, TaskStatus.REVIEW.value]:
                continue
            
            can_start, reason = self._check_can_start(task)
            
            if can_start:
                if task.status != TaskStatus.READY.value:
                    task.status = TaskStatus.READY.value
                    task.blocked_reason = ""
            else:
                task.status = TaskStatus.PENDING.value
                task.blocked_reason = reason
    
    def start_task(self, task_id: str) -> tuple[bool, str]:
        """启动一个任务"""
        task = self.get_task(task_id)
        if not task:
            return False, f"Task {task_id} not found"
        
        can_start, reason = self._check_can_start(task)
        if not can_start:
            return False, reason
        
        agent = self.agents[task.assignee]
        agent.assign_task(task_id)
        
        task.status = TaskStatus.IN_PROGRESS.value
        task.started_at = datetime.now().isoformat()
        
        self._log_event("TASK_STARTED", task)
        return True, f"Task {task_id} started by {task.assignee}"
    
    def complete_task(self, task_id: str, outputs: List[Dict] = None) -> tuple[bool, str]:
        """完成任务"""
        task = self.get_task(task_id)
        if not task:
            return False, f"Task {task_id} not found"
        
        if task.status != TaskStatus.IN_PROGRESS.value:
            return False, f"Task {task_id} is not in progress"
        
        agent = self.agents[task.assignee]
        agent.complete_task(task_id)
        
        task.status = TaskStatus.COMPLETED.value
        task.completed_at = datetime.now().isoformat()
        
        if outputs:
            task.outputs = [TaskOutput(**o) for o in outputs]
        
        self._evaluate_ready_tasks()
        
        self._log_event("TASK_COMPLETED", task)
        
        self._notify_dependent_tasks(task_id)
        
        return True, f"Task {task_id} completed"
    
    def _notify_dependent_tasks(self, completed_task_id: str):
        """通知依赖此任务的其他任务"""
        for task in self.tasks.values():
            if completed_task_id in task.blocked_by:
                self._log_event("DEPENDENCY_UNBLOCKED", {
                    "task_id": task.task_id,
                    "unblocked_by": completed_task_id
                })
    
    def _log_event(self, event_type: str, data):
        """记录事件"""
        if isinstance(data, Task):
            data = data.to_dict()
        
        self.task_history.append({
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
    
    def auto_schedule(self) -> Dict[str, List[str]]:
        """自动调度所有可执行的任务"""
        self._evaluate_ready_tasks()
        
        ready_tasks = self.get_ready_tasks()
        started = {}
        
        for task in ready_tasks:
            success, msg = self.start_task(task.task_id)
            if success:
                if task.assignee not in started:
                    started[task.assignee] = []
                started[task.assignee].append(task.task_id)
        
        return started
    
    def get_sprint_board(self) -> Dict[str, List[Dict]]:
        """获取Sprint看板视图"""
        board = {
            "TODO": [],
            "IN_PROGRESS": [],
            "REVIEW": [],
            "COMPLETED": [],
            "BLOCKED": []
        }
        
        for task in self.tasks.values():
            item = {
                "task_id": task.task_id,
                "title": task.title,
                "assignee": task.assignee.split("_")[0].upper(),
                "priority": task.priority,
                "time_estimate": task.time_estimate,
                "blocked_reason": task.blocked_reason if task.status == "blocked" else ""
            }
            
            if task.status == TaskStatus.PENDING.value:
                board["TODO"].append(item)
            elif task.status == TaskStatus.READY.value:
                board["TODO"].append(item)
            elif task.status == TaskStatus.IN_PROGRESS.value:
                board["IN_PROGRESS"].append(item)
            elif task.status == TaskStatus.REVIEW.value:
                board["REVIEW"].append(item)
            elif task.status == TaskStatus.COMPLETED.value:
                board["COMPLETED"].append(item)
            elif task.status == TaskStatus.BLOCKED.value:
                board["BLOCKED"].append(item)
        
        return board
    
    def get_team_workload(self) -> Dict[str, Dict]:
        """获取团队工作负载"""
        workload = {}
        
        for agent_id, agent in self.agents.items():
            workload[agent_id] = {
                "name": agent.name,
                "current_tasks": agent.current_tasks,
                "completed_tasks": len(agent.completed_tasks),
                "max_parallel": agent.max_parallel,
                "workload_percent": int(agent.workload * 100)
            }
        
        return workload
    
    def generate_daily_standup(self) -> str:
        """生成每日站会报告"""
        board = self.get_sprint_board()
        workload = self.get_team_workload()
        
        lines = [
            "# 时光树 M1 Sprint 每日站会",
            f"## 日期: {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "## 各Agent进度",
            ""
        ]
        
        for agent_id, data in workload.items():
            lines.append(f"### {data['name']}")
            current = data['current_tasks']
            if current:
                lines.append(f"- 进行中: {', '.join(current)}")
            else:
                lines.append("- 进行中: 无")
            lines.append(f"- 已完成: {data['completed_tasks']} 个任务")
            lines.append(f"- 负载率: {data['workload_percent']}%")
            lines.append("")
        
        lines.extend([
            "## 看板概览",
            f"- TODO: {len(board['TODO'])} 个任务",
            f"- 进行中: {len(board['IN_PROGRESS'])} 个任务",
            f"- Review: {len(board['REVIEW'])} 个任务",
            f"- 已完成: {len(board['COMPLETED'])} 个任务",
            f"- 阻塞: {len(board['BLOCKED'])} 个任务",
            ""
        ])
        
        blocked = board['BLOCKED']
        if blocked:
            lines.append("## 阻塞任务")
            for task in blocked:
                lines.append(f"- {task['task_id']}: {task['title']} ({task['blocked_reason']})")
        
        return "\n".join(lines)
    
    def export_tasks_json(self, filepath: str):
        """导出任务为JSON"""
        tasks_data = {
            "export_time": datetime.now().isoformat(),
            "sprint": "M1",
            "total_tasks": len(self.tasks),
            "tasks": [t.to_dict() for t in self.tasks.values()]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)
    
    def simulate_day(self, day: int):
        """模拟一天的开发过程"""
        print(f"\n{'='*60}")
        print(f"模拟第 {day} 天开发")
        print(f"{'='*60}")
        
        started = self.auto_schedule()
        
        for agent_id, tasks in started.items():
            agent = self.agents[agent_id]
            print(f"\n{agent.name} 开始任务:")
            for task_id in tasks:
                task = self.get_task(task_id)
                print(f"  - {task_id}: {task.title}")
        
        if not started:
            print("\n无可启动的新任务")
        
        completed_tasks = []
        for task in self.get_in_progress_tasks():
            import random
            if random.random() > 0.5:
                success, msg = self.complete_task(task.task_id)
                if success:
                    completed_tasks.append(task.task_id)
        
        if completed_tasks:
            print(f"\n完成的任务:")
            for task_id in completed_tasks:
                print(f"  - {task_id}")
        
        print(f"\n团队负载:")
        for agent_id, data in self.get_team_workload().items():
            print(f"  {data['name']}: {data['workload_percent']}% "
                  f"({len(data['current_tasks'])}/{data['max_parallel']})")


def main():
    system = AgentCollaborationSystem()
    
    print("时光树 M1 阶段 Agent 协作任务系统")
    print("=" * 50)
    print(f"总任务数: {len(system.tasks)}")
    print(f"Agent数量: {len(system.agents)}")
    
    print("\n初始化工完成，开始自动调度...")
    
    for day in range(1, 8):
        system.simulate_day(day)
    
    print("\n" + "=" * 50)
    print("Sprint 看板")
    print("=" * 50)
    
    board = system.get_sprint_board()
    for column, tasks in board.items():
        print(f"\n{column} ({len(tasks)}):")
        for task in tasks[:5]:
            print(f"  [{task['task_id']}] {task['title'][:30]}...")
        if len(tasks) > 5:
            print(f"  ... 还有 {len(tasks) - 5} 个任务")
    
    print("\n" + "=" * 50)
    print("每日站会报告")
    print("=" * 50)
    print(system.generate_daily_standup())
    
    system.export_tasks_json("/workspace/tasks_m1_sprint.json")
    print("\n任务已导出到 /workspace/tasks_m1_sprint.json")


if __name__ == "__main__":
    main()
