# 时光树 - 后端 API 详细设计

| 属性 | 内容 |
|------|------|
| 产品名称 | 时光树 |
| 端 | Go API 服务 |
| 版本 | v1.0 |
| 创建日期 | 2026-04-02 |

---

## 一、API 设计规范

### 1.1 REST API 规范

| 规范 | 说明 |
|------|------|
| 基础路径 | `/api/v1` |
| 认证方式 | Bearer Token (JWT) |
| 请求格式 | `Content-Type: application/json` |
| 响应格式 | JSON |
| 字符编码 | UTF-8 |
| 时间格式 | RFC3339 (ISO8601) |

### 1.2 通用响应结构

```json
{
  "code": 0,
  "message": "success",
  "data": {},
  "request_id": "uuid"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | 状态码，0=成功，非0=失败 |
| message | string | 错误信息 |
| data | object | 响应数据 |
| request_id | string | 请求追踪ID |

### 1.3 分页响应

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "has_more": true
  }
}
```

### 1.4 错误码定义

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 缺少必需参数 |
| 1003 | 参数格式错误 |
| 2001 | 未认证 |
| 2002 | Token过期 |
| 2003 | 无权限 |
| 3001 | 资源不存在 |
| 3002 | 资源已存在 |
| 3003 | 操作被禁止 |
| 4001 | 系统错误 |
| 4002 | 服务降级 |
| 5001 | 业务错误 |

---

## 二、用户与认证 API

### 2.1 发送验证码

```
POST /api/v1/auth/sendCode
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| phone | string | 是 | 手机号 |
| type | string | 是 | 场景：login/register/bind |

**请求示例**

```json
{
  "phone": "13800138000",
  "type": "login"
}
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "expires_in": 300
  }
}
```

### 2.2 验证码登录

```
POST /api/v1/auth/login
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| phone | string | 是 | 手机号 |
| code | string | 是 | 验证码 |
| device_id | string | 是 | 设备ID |
| device_name | string | 否 | 设备名称 |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 86400,
    "user": {
      "id": "uuid",
      "phone": "13800138000",
      "nickname": "",
      "avatar": "",
      "create_at": "2026-04-02T10:00:00Z"
    }
  }
}
```

### 2.3 微信登录

```
POST /api/v1/auth/wechat
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 微信授权code |
| device_id | string | 是 | 设备ID |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "expires_in": 86400,
    "is_new_user": true,
    "user": {
      "id": "uuid",
      "nickname": "微信用户",
      "avatar": "https://..."
    }
  }
}
```

### 2.4 绑定手机号

```
POST /api/v1/auth/bindPhone
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| phone | string | 是 | 手机号 |
| code | string | 是 | 验证码 |

### 2.5 获取用户信息

```
GET /api/v1/user/profile
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "uuid",
    "phone": "13800138000",
    "nickname": "用户昵称",
    "avatar": "https://...",
    "gender": "unknown",
    "birthday": null,
    "lives": [
      {
        "id": "life_uuid",
        "life_type": "infant",
        "nickname": "宝宝",
        "birth_date": "2025-01-01",
        "current_stage": "infant",
        "is_active": true
      }
    ],
    "families": [
      {
        "id": "family_uuid",
        "name": "我的家庭",
        "role": "owner"
      }
    ]
  }
}
```

### 2.6 更新用户信息

```
PUT /api/v1/user/profile
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nickname | string | 否 | 昵称 |
| avatar | string | 否 | 头像URL |
| gender | string | 否 | 性别：male/female/unknown |
| birthday | string | 否 | 生日 YYYY-MM-DD |

### 2.7 设备管理

```
GET /api/v1/user/devices
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "uuid",
        "device_id": "device_xxx",
        "device_name": "iPhone 15",
        "device_type": "ios",
        "last_active_at": "2026-04-02T10:00:00Z",
        "is_current": true
      }
    ]
  }
}
```

### 2.8 注销账号

```
POST /api/v1/user/destroy
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| code | string | 是 | 验证码确认 |

---

## 三、生命管理 API

### 3.1 创建生命

```
POST /api/v1/life
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_type | string | 是 | 生命类型：fetus/baby/child |
| nickname | string | 否 | 昵称 |
| birth_date | string | 否 | 出生日期（已出生） |
| due_date | string | 否 | 预产期（孕期） |
| mother_name | string | 否 | 妈妈姓名 |
| gender | string | 否 | 性别：male/female/unknown |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "life_uuid",
    "life_type": "fetus",
    "nickname": "小宝宝",
    "due_date": "2026-10-01",
    "gestation_week": 8,
    "current_stage": "fetus",
    "stage_start_date": "2026-04-02",
    "create_at": "2026-04-02T10:00:00Z"
  }
}
```

### 3.2 获取当前生命

```
GET /api/v1/life/current
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "life_uuid",
    "life_type": "fetus",
    "nickname": "小宝宝",
    "birth_date": null,
    "due_date": "2026-10-01",
    "gestation_week": 8,
    "current_stage": "fetus",
    "stage_history": [
      {
        "stage": "fetus",
        "start_date": "2026-04-02",
        "end_date": null
      }
    ],
    "metadata": {
      "mother_name": "妈妈"
    }
  }
}
```

### 3.3 获取用户所有生命

```
GET /api/v1/life/list
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "life_uuid_1",
        "life_type": "fetus",
        "nickname": "二宝",
        "is_active": true,
        "current_stage": "fetus"
      },
      {
        "id": "life_uuid_2",
        "life_type": "child",
        "nickname": "大宝",
        "birth_date": "2020-01-01",
        "is_active": false,
        "current_stage": "child"
      }
    ]
  }
}
```

### 3.4 更新生命信息

```
PUT /api/v1/life/{life_id}
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| nickname | string | 否 | 昵称 |
| birth_date | string | 否 | 出生日期 |
| due_date | string | 否 | 预产期 |
| gender | string | 否 | 性别 |
| metadata | object | 否 | 扩展信息 |

### 3.5 更新生命阶段

```
PUT /api/v1/life/{life_id}/stage
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| stage | string | 是 | 目标阶段 |

**阶段枚举**

| 阶段 | 说明 |
|------|------|
| fetus | 孕期 |
| infant | 婴儿期（0-1岁） |
| toddler | 幼儿期（1-3岁） |
| child | 学龄期（3-12岁） |
| teen | 青少年期（12-18岁） |
| adult | 成年期（18-60岁） |
| elder | 老年期（60岁+） |

### 3.6 切换当前生命

```
POST /api/v1/life/{life_id}/activate
```

---

## 四、家庭管理 API

### 4.1 创建家庭

```
POST /api/v1/family
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | 是 | 家庭名称 |
| family_type | string | 否 | 家庭类型 |

**family_type 枚举**

| 类型 | 说明 |
|------|------|
| nuclear | 核心家庭 |
| extended | 大家庭 |
| single_parent | 单亲家庭 |
| blended | 重组家庭 |
| grandparent_only | 祖孙家庭 |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "family_uuid",
    "name": "我的家庭",
    "family_type": "nuclear",
    "invite_code": "ABC123",
    "owner_life_id": "life_uuid",
    "member_count": 1,
    "create_at": "2026-04-02T10:00:00Z"
  }
}
```

### 4.2 获取家庭信息

```
GET /api/v1/family/{family_id}
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "family_uuid",
    "name": "我的家庭",
    "family_type": "nuclear",
    "avatar": null,
    "owner_life_id": "life_uuid",
    "settings": {
      "allow_invite": true,
      "require_approval": false,
      "max_members": 20
    },
    "create_at": "2026-04-02T10:00:00Z"
  }
}
```

### 4.3 获取家庭成员列表

```
GET /api/v1/family/{family_id}/members
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "member_uuid",
        "life_id": "life_uuid",
        "nickname": "爸爸",
        "avatar": "https://...",
        "role": "owner",
        "relationship": "father",
        "family_nickname": "爸爸",
        "join_at": "2026-04-02T10:00:00Z",
        "status": "active"
      }
    ],
    "total": 3
  }
}
```

### 4.4 生成邀请码

```
POST /api/v1/family/{family_id}/invite
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| expire_hours | int | 否 | 过期时间（小时），默认72 |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "invite_code": "ABC123",
    "invite_link": "shiguangshu://join/ABC123",
    "expire_at": "2026-04-05T10:00:00Z"
  }
}
```

### 4.5 加入家庭

```
POST /api/v1/family/join
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| invite_code | string | 是 | 邀请码 |
| relationship | string | 是 | 与户主关系 |
| nickname | string | 否 | 家庭内昵称 |

### 4.6 更新家庭成员

```
PUT /api/v1/family/{family_id}/member/{member_id}
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| family_nickname | string | 否 | 家庭昵称 |
| role | string | 否 | 角色（仅owner可操作） |

### 4.7 退出家庭

```
DELETE /api/v1/family/{family_id}/member/{member_id}
```

### 4.8 解散家庭

```
DELETE /api/v1/family/{family_id}
```

---

## 五、时间轴 API

### 5.1 获取时间轴列表

```
GET /api/v1/timeline
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| stage_type | string | 否 | 阶段筛选 |
| space_type | string | 否 | 空间类型：public/private |
| event_type | string | 否 | 事件类型 |
| start_date | string | 否 | 开始日期 |
| end_date | string | 否 | 结束日期 |
| owner_life_id | string | 否 | 发布者生命ID |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认20 |

**event_type 枚举**

| 类型 | 说明 |
|------|------|
| growth | 成长 |
| health | 健康 |
| education | 教育 |
| emotion | 情绪 |
| family | 家庭 |
| milestone | 里程碑 |
| custom | 自定义 |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "timeline_uuid",
        "life_id": "life_uuid",
        "event_type": "growth",
        "stage_type": "fetus",
        "title": "第一次产检",
        "description": "今天去做了第一次产检，一切正常",
        "event_date": "2026-04-02",
        "space_type": "public",
        "owner_life_id": "life_uuid",
        "tags": ["产检", "重要"],
        "emotion": "positive",
        "emotion_score": 0.85,
        "media": [
          {
            "id": "media_uuid",
            "content_type": "photo",
            "url": "https://...",
            "thumbnail_url": "https://..."
          }
        ],
        "ai_summary": "第一次产检记录，孕妇状态良好",
        "created_at": "2026-04-02T10:00:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "has_more": true
  }
}
```

### 5.2 发布时间轴

```
POST /api/v1/timeline
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| event_type | string | 是 | 事件类型 |
| title | string | 是 | 标题 |
| description | string | 否 | 描述 |
| event_date | string | 是 | 事件日期 |
| space_type | string | 是 | 空间类型：public/private |
| tags | string[] | 否 | 标签 |
| emotion | string | 否 | 情绪标签 |
| media_ids | string[] | 否 | 媒体ID列表 |
| milestone_refs | string[] | 否 | 关联里程碑 |
| knowledge_refs | string[] | 否 | 关联知识 |

### 5.3 获取时间轴详情

```
GET /api/v1/timeline/{timeline_id}
```

### 5.4 更新时间轴

```
PUT /api/v1/timeline/{timeline_id}
```

### 5.5 删除时间轴

```
DELETE /api/v1/timeline/{timeline_id}
```

### 5.6 点赞时间轴

```
POST /api/v1/timeline/{timeline_id}/like
```

### 5.7 评论时间轴

```
GET /api/v1/timeline/{timeline_id}/comments
POST /api/v1/timeline/{timeline_id}/comment
DELETE /api/v1/timeline/{timeline_id}/comment/{comment_id}
```

---

## 六、内容管理 API

### 6.1 上传内容

```
POST /api/v1/content/upload
Content-Type: multipart/form-data
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 文件 |
| life_id | string | 是 | 生命ID |
| content_type | string | 是 | 内容类型：photo/video/audio/file |
| space_type | string | 是 | 空间类型 |
| stage_type | string | 否 | 阶段类型 |
| event_id | string | 否 | 关联事件ID |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "content_uuid",
    "content_type": "photo",
    "url": "https://...",
    "thumbnail_url": "https://...",
    "file_size": 1024000,
    "ai_tags": ["宝宝", "微笑"],
    "ai_description": "一个微笑的宝宝"
  }
}
```

### 6.2 批量上传

```
POST /api/v1/content/upload/batch
Content-Type: multipart/form-data
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| files | file[] | 是 | 文件列表（最多9个） |
| life_id | string | 是 | 生命ID |
| space_type | string | 是 | 空间类型 |

### 6.3 获取内容

```
GET /api/v1/content/{content_id}
```

### 6.4 删除内容

```
DELETE /api/v1/content/{content_id}
```

### 6.5 获取内容列表

```
GET /api/v1/content/list
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| space_type | string | 否 | 空间类型 |
| content_type | string | 否 | 内容类型 |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

---

## 七、知识库 API

### 7.1 创建知识条目

```
POST /api/v1/knowledge
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| knowledge_type | string | 是 | 知识类型 |
| title | string | 是 | 标题 |
| content | string | 是 | 内容 |
| space_type | string | 是 | 空间类型 |
| tags | string[] | 否 | 标签 |
| category | string | 否 | 分类 |
| related_timeline_ids | string[] | 否 | 关联时间轴 |
| is_milestone | bool | 否 | 是否里程碑 |
| is_family_heritage | bool | 否 | 是否家庭传承 |

**knowledge_type 枚举**

| 类型 | 说明 |
|------|------|
| note | 笔记 |
| book | 书摘 |
| skill | 技能 |
| decision | 重要决定 |
| reflection | 反思 |
| family_story | 家庭故事 |

### 7.2 获取知识列表

```
GET /api/v1/knowledge
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| knowledge_type | string | 否 | 知识类型 |
| space_type | string | 否 | 空间类型 |
| is_family_heritage | bool | 否 | 仅传承 |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

### 7.3 获取知识详情

```
GET /api/v1/knowledge/{knowledge_id}
```

### 7.4 更新知识

```
PUT /api/v1/knowledge/{knowledge_id}
```

### 7.5 删除知识

```
DELETE /api/v1/knowledge/{knowledge_id}
```

---

## 八、私密日记 API

### 8.1 创建日记

```
POST /api/v1/diary
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| title | string | 否 | 标题 |
| content | string | 是 | 内容 |
| mood | string | 否 | 心情 |
| weather | string | 否 | 天气 |
| location | string | 否 | 位置 |
| media_ids | string[] | 否 | 媒体ID |
| tags | string[] | 否 | 标签 |

### 8.2 获取日记列表

```
GET /api/v1/diary
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| start_date | string | 否 | 开始日期 |
| end_date | string | 否 | 结束日期 |
| mood | string | 否 | 心情筛选 |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "diary_uuid",
        "life_id": "life_uuid",
        "title": "今天的感受",
        "content_preview": "今天宝宝踢了我一下...",
        "mood": "happy",
        "emotion_score": 0.9,
        "ai_insights": "今天情绪积极，与宝宝互动良好",
        "has_media": true,
        "created_at": "2026-04-02T10:00:00Z"
      }
    ],
    "total": 50,
    "page": 1,
    "page_size": 20,
    "has_more": true
  }
}
```

### 8.3 获取日记详情

```
GET /api/v1/diary/{diary_id}
```

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "diary_uuid",
    "life_id": "life_uuid",
    "title": "今天的感受",
    "content": "今天宝宝踢了我一下，感觉特别幸福...",
    "mood": "happy",
    "weather": "sunny",
    "location": "家里",
    "emotion_score": 0.9,
    "ai_insights": "今天情绪积极，与宝宝互动良好",
    "media": [
      {
        "id": "media_uuid",
        "content_type": "photo",
        "url": "https://..."
      }
    ],
    "tags": ["孕期", "幸福"],
    "created_at": "2026-04-02T10:00:00Z"
  }
}
```

### 8.4 更新日记

```
PUT /api/v1/diary/{diary_id}
```

### 8.5 删除日记

```
DELETE /api/v1/diary/{diary_id}
```

### 8.6 获取情绪趋势

```
GET /api/v1/diary/{life_id}/emotion-trend
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| start_date | string | 是 | 开始日期 |
| end_date | string | 是 | 结束日期 |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "trend": [
      {"date": "2026-04-01", "score": 0.8, "mood": "happy"},
      {"date": "2026-04-02", "score": 0.9, "mood": "happy"}
    ],
    "average_score": 0.85,
    "dominant_mood": "happy",
    "summary": "近7天情绪整体积极稳定"
  }
}
```

---

## 九、AI 服务 API

### 9.1 AI 对话

```
POST /api/v1/ai/chat
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| message | string | 是 | 用户消息 |
| session_id | string | 否 | 会话ID |
| ai_type | string | 否 | AI类型：family/personal，默认personal |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "session_id": "session_uuid",
    "reply": "今天宝宝的状态看起来很棒呢！",
    "ai_type": "personal",
    "context_related": true
  }
}
```

### 9.2 内容摘要

```
POST /api/v1/ai/summary
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | string | 是 | 内容 |
| type | string | 是 | 类型：text/image/diary |

### 9.3 情绪分析

```
POST /api/v1/ai/emotion
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| content | string | 是 | 内容 |
| type | string | 是 | 类型：text/diary/mood |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "emotion": "happy",
    "score": 0.85,
    "intensity": "moderate",
    "insights": "整体情绪积极，可能与孕期激素变化有关"
  }
}
```

### 9.4 成长建议

```
GET /api/v1/ai/growth-suggest
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| stage_type | string | 否 | 阶段类型 |

### 9.5 AI 生成内容

```
POST /api/v1/ai/generate
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| type | string | 是 | 生成类型 |
| params | object | 是 | 生成参数 |

**type 枚举**

| 类型 | 说明 |
|------|------|
| weekly_report | 周报 |
| monthly_report | 月报 |
| growth_summary | 成长总结 |
| memory_video | 回忆视频脚本 |
| milestone_story | 里程碑故事 |

---

## 十、插件管理 API

### 10.1 获取插件列表

```
GET /api/v1/plugins
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 否 | 生命ID |
| stage_type | string | 否 | 阶段类型 |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": "prenatal",
        "name": "孕期助手",
        "version": "1.0.0",
        "stage_type": "fetus",
        "icon": "https://...",
        "is_recommended": true,
        "is_installed": true,
        "status": "active"
      },
      {
        "id": "infant",
        "name": "婴儿期助手",
        "version": "1.0.0",
        "stage_type": "infant",
        "icon": "https://...",
        "is_recommended": true,
        "is_installed": false,
        "status": "not_installed"
      }
    ]
  }
}
```

### 10.2 安装插件

```
POST /api/v1/plugins/{plugin_id}/install
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |

### 10.3 卸载插件

```
POST /api/v1/plugins/{plugin_id}/uninstall
```

### 10.4 获取插件数据

```
GET /api/v1/plugins/{plugin_id}/data
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| data_type | string | 否 | 数据类型 |

### 10.5 保存插件数据

```
POST /api/v1/plugins/{plugin_id}/data
```

---

## 十一、数据导出与销毁 API

### 11.1 申请数据导出

```
POST /api/v1/data/export
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| format | string | 否 | 格式：json/pdf/zip，默认json |

**响应示例**

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "task_id": "task_uuid",
    "status": "processing",
    "estimate_time": 300
  }
}
```

### 11.2 获取导出进度

```
GET /api/v1/data/export/{task_id}
```

### 11.3 下载导出数据

```
GET /api/v1/data/export/{task_id}/download
```

### 11.4 申请数据销毁

```
POST /api/v1/data/destroy
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| code | string | 是 | 验证码确认 |

### 11.5 设置传承

```
POST /api/v1/data/heritage
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| inherit_to | string[] | 是 | 继承者LifeID列表 |
| inheritance_type | string | 否 | 传承方式：auto/manual |
| expire_at | string | 否 | 失效时间 |

---

## 十二、消息通知 API

### 12.1 获取通知列表

```
GET /api/v1/notifications
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| life_id | string | 是 | 生命ID |
| type | string | 否 | 通知类型 |
| is_read | bool | 否 | 已读状态 |
| page | int | 否 | 页码 |
| page_size | int | 否 | 每页数量 |

### 12.2 标记已读

```
POST /api/v1/notifications/mark-read
```

**请求参数**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| notification_ids | string[] | 是 | 通知ID列表 |

### 12.3 删除通知

```
DELETE /api/v1/notifications/{notification_id}
```

### 12.4 获取未读数

```
GET /api/v1/notifications/unread-count
```

---

## 十三、WebSocket API

### 13.1 连接

```
WS /api/v1/ws/connect
```

**连接参数**

| 参数 | 说明 |
|------|------|
| token | JWT Token |
| life_id | 当前生命ID |

### 13.2 消息类型

| 类型 | 说明 | 方向 |
|------|------|------|
| timeline.new | 新时间轴 | Server→Client |
| timeline.like | 点赞通知 | Server→Client |
| timeline.comment | 评论通知 | Server→Client |
| family.member_joined | 新成员加入 | Server→Client |
| family.member_left | 成员离开 | Server→Client |
| ai.response | AI回复 | Server→Client |
| stage.transition | 阶段切换提醒 | Server→Client |
| reminder.trigger | 提醒触发 | Server→Client |

### 13.3 消息格式

```json
{
  "type": "timeline.new",
  "data": {
    "timeline_id": "uuid",
    "from_life_id": "uuid",
    "from_nickname": "爸爸"
  },
  "timestamp": "2026-04-02T10:00:00Z"
}
```
