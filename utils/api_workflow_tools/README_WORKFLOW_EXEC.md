2025-12-23 17:38:06.028 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-1510b4b0] 任务函数执行完成: job_id=1
2025-12-23 17:38:06.192 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-1510b4b0] 释放任务锁: job_id=1
2025-12-23 17:38:06.193 |  | WARNING  | config.get_scheduler:scheduler_event_listener:699 - [Scheduler] 任务延迟执行: job_id=1, 计划时间=17:38:00, 实际时间=17:38:06, 延迟=6.2秒
2025-12-23 17:38:09.758 | 63f3efa428c2427698e65ebafad46761 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:query_detail_report_api_workflow_report:104 - id:<built-in function id>
2025-12-23 17:38:09.771 | 63f3efa428c2427698e65ebafad46761 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:query_detail_report_api_workflow_report:107 - 获取report_id为4113的信息成功
2025-12-23 17:38:09.776 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/4113 - 200 - 196.63ms
INFO:     127.0.0.1:61971 - "GET /report/api_workflow_report/4113 HTTP/1.1" 200 OK
2025-12-23 17:38:25.215 |  | ERROR    | config.get_websocket:listener:86 - [PID:33344] Pub/Sub 监听异常: Timed out closing connection after 15，5秒后重连...
2025-12-23 17:38:25.290 |  | INFO     | config.get_websocket:disconnect:212 - [PID:33344] WebSocket连接断开: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification, user_id=1, 本进程连接数: 0
INFO:     connection closed
2025-12-23 17:38:25.481 | 666177af65d2403ba30fe6b118d67636 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
INFO:     127.0.0.1:54656 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:38:25.501 | 666177af65d2403ba30fe6b118d67636 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:38:25.506 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 274.25ms
2025-12-23 17:38:25.638 | 59b34778539f42868dd9157fda36909c | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:38:25.645 | 59b34778539f42868dd9157fda36909c | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:38:25.647 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 135.52ms
INFO:     127.0.0.1:61214 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:38:25.713 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:38:25.714 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:38:25.715 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:38:25.717 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:38:25.717 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:38:25.717 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:38:25.751 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:38:25.751 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:38:25.751 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:38:25.859 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:38:25.863 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:38:25.907 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:38:25.908 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:38:25.909 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:38:25.992 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:26.018 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:38:26.051 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:26.051 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
INFO:     127.0.0.1:65425 - "WebSocket /ws/connect/notification?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjkxNjYzOWRmLTM1MmItNDU2MC1hMTg5LTcxNjBiZmZmYmY2ZiIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTI3LjAuMC4xIiwibG9naW5Mb2NhdGlvbiI6Ilx1NTE4NVx1N2Y1MUlQIiwiYnJvd3NlciI6IkNocm9tZSAxNDMuMC4wIiwib3MiOiJXaW5kb3dzIDEwIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAwOToxNDoxNiJ9LCJleHAiOjE3NjY1Mzg4NTd9.8AUwzx694I3W_TwW9juA6FYN2Mu_7jcOpZFNCwZYGIQ" [accepted]
INFO:     connection open
2025-12-23 17:38:26.401 |  | INFO     | config.get_websocket:connect:180 - [PID:22756] WebSocket连接建立: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification, user_id=1, 本进程连接数: 1
2025-12-23 17:38:26.403 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:38:26.986 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.934s
2025-12-23 17:38:26.986 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9348266124725342
2025-12-23 17:38:26.987 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjUwYzhiNTYxLTBmZWEtNDNjMi04ZmRkLTY0OWNiODU0ODdjMyIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODoyNyJ9LCJleHAiOjE3NjY1NjkxMDd9.ZBWfFSnap4K57DJjqSMc0HDK-aOc5bWmkRYeDWhoGfc']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjUwYzhiNTYxLTBmZWEtNDNjMi04ZmRkLTY0OWNiODU0ODdjMyIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODoyNyJ9LCJleHAiOjE3NjY1NjkxMDd9.ZBWfFSnap4K57DJjqSMc0HDK-aOc5bWmkRYeDWhoGfc
2025-12-23 17:38:27.049 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjUwYzhiNTYxLTBmZWEtNDNjMi04ZmRkLTY0OWNiODU0ODdjMyIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODoyNyJ9LCJleHAiOjE3NjY1NjkxMDd9.ZBWfFSnap4K57DJjqSMc0HDK-aOc5bWmkRYeDWhoGfc', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjUwYzhiNTYxLTBmZWEtNDNjMi04ZmRkLTY0OWNiODU0ODdjMyIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODoyNyJ9LCJleHAiOjE3NjY1NjkxMDd9.ZBWfFSnap4K57DJjqSMc0HDK-aOc5bWmkRYeDWhoGfc'}, 'execution_time': 0.059468746185302734, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjUwYzhiNTYxLTBmZWEtNDNjMi04ZmRkLTY0OWNiODU0ODdjMyIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODoyNyJ9LCJleHAiOjE3NjY1NjkxMDd9.ZBWfFSnap4K57DJjqSMc0HDK-aOc5bWmkRYeDWhoGfc'}}
2025-12-23 17:38:27.049 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:38:27.050 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.140s
2025-12-23 17:38:27.050 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:38:27.064 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:27.064 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:38:27.065 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:38:27.065 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:38:27.163 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:27.191 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:27.191 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:28.278 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.086s
2025-12-23 17:38:28.278 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0865285396575928
2025-12-23 17:38:28.278 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:28.278 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:28.279 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.213s
2025-12-23 17:38:28.279 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:38:28.289 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:28.290 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:38:28.290 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:38:28.369 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:28.396 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:28.397 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:28.650 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.253s
2025-12-23 17:38:28.650 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.25299596786499023
2025-12-23 17:38:28.650 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:28.650 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:28.651 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.361s
2025-12-23 17:38:28.651 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:38:28.656 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:28.656 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:38:28.656 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:38:28.720 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:28.745 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:28.745 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:29.146 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.401s
2025-12-23 17:38:29.146 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.401090145111084
2025-12-23 17:38:29.147 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:29.147 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:29.147 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.491s
2025-12-23 17:38:29.147 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:38:29.154 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:29.154 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:38:29.154 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:38:29.250 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:29.274 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:29.275 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:29.536 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.261s
2025-12-23 17:38:29.536 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.261432409286499
2025-12-23 17:38:29.536 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:29.537 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:29.537 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.383s
2025-12-23 17:38:29.537 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:38:29.547 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:29.548 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:38:29.548 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:38:29.621 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:29.644 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:29.644 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:29.932 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.287s
2025-12-23 17:38:29.933 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2886326313018799
2025-12-23 17:38:29.933 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:29.933 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:29.933 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.385s
2025-12-23 17:38:29.933 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:38:29.940 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:29.941 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:38:29.941 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:38:30.027 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:30.058 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:30.060 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:30.233 |  | INFO     | config.get_websocket:listener:76 - [PID:33344] 已订阅 Redis 频道: websocket:broadcast:dev
2025-12-23 17:38:31.062 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.002s
2025-12-23 17:38:31.062 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0022945404052734
2025-12-23 17:38:31.062 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:31.063 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:31.063 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.121s
2025-12-23 17:38:31.063 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:38:31.071 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:31.071 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:38:31.071 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:38:31.155 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:31.182 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:38:31.182 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:31.443 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.261s
2025-12-23 17:38:31.443 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2609379291534424
2025-12-23 17:38:31.444 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:38:31.444 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:31.444 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.372s
2025-12-23 17:38:31.445 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:38:31.450 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:31.454 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:38:31.522 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:38:31.522 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:38:31.524 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:38:31.524 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:38:31.530 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.74秒
2025-12-23 17:38:31.532 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:38:31.672 | c033aa4b92094423ae97ec87adad085a | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
2025-12-23 17:38:31.704 | c033aa4b92094423ae97ec87adad085a | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:38:31.705 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 168.53ms
2025-12-23 17:38:31.713 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
INFO:     127.0.0.1:62176 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:38:32.152 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:38:32.152 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:38:32.152 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:38:32.152 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:38:32.153 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:38:32.153 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:38:32.173 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:38:32.174 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:38:32.174 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:38:32.304 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:38:32.307 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:38:32.335 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:38:32.335 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:38:32.335 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:38:32.408 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:32.445 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:38:32.482 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:32.482 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:33.388 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.906s
2025-12-23 17:38:33.388 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9055731296539307
2025-12-23 17:38:33.389 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjQyYzRmNTFjLTEzY2QtNGYyZC04ODVjLTMzOGJhMzUyZDBhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozMyJ9LCJleHAiOjE3NjY1NjkxMTR9.GM662L6Xum_oyCR_ci4hPHTitb91z1-VMjN3ZxNs13Y']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjQyYzRmNTFjLTEzY2QtNGYyZC04ODVjLTMzOGJhMzUyZDBhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozMyJ9LCJleHAiOjE3NjY1NjkxMTR9.GM662L6Xum_oyCR_ci4hPHTitb91z1-VMjN3ZxNs13Y
2025-12-23 17:38:33.449 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjQyYzRmNTFjLTEzY2QtNGYyZC04ODVjLTMzOGJhMzUyZDBhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozMyJ9LCJleHAiOjE3NjY1NjkxMTR9.GM662L6Xum_oyCR_ci4hPHTitb91z1-VMjN3ZxNs13Y', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjQyYzRmNTFjLTEzY2QtNGYyZC04ODVjLTMzOGJhMzUyZDBhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozMyJ9LCJleHAiOjE3NjY1NjkxMTR9.GM662L6Xum_oyCR_ci4hPHTitb91z1-VMjN3ZxNs13Y'}, 'execution_time': 0.05989694595336914, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjQyYzRmNTFjLTEzY2QtNGYyZC04ODVjLTMzOGJhMzUyZDBhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozMyJ9LCJleHAiOjE3NjY1NjkxMTR9.GM662L6Xum_oyCR_ci4hPHTitb91z1-VMjN3ZxNs13Y'}}
2025-12-23 17:38:33.449 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:38:33.449 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.114s
2025-12-23 17:38:33.450 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:38:33.458 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:33.459 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:38:33.459 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:38:33.459 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:38:33.545 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:33.579 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:33.579 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:33.605 | 46fb1ec8342146e1b3a7818e8b7f6df2 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:38:33.612 | 46fb1ec8342146e1b3a7818e8b7f6df2 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:38:33.615 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 139.72ms
INFO:     127.0.0.1:63516 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:38:34.515 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.935s
2025-12-23 17:38:34.517 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9371788501739502
2025-12-23 17:38:34.517 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:34.517 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:34.518 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.059s
2025-12-23 17:38:34.518 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:38:34.525 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:34.526 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:38:34.526 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:38:34.630 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:34.667 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:34.667 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:34.912 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.245s
2025-12-23 17:38:34.912 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.24481964111328125
2025-12-23 17:38:34.913 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:34.913 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:34.913 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.387s
2025-12-23 17:38:34.913 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:38:34.919 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:34.919 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:38:34.919 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:38:34.989 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:35.000 | 502e999363d14e19b2ecac556be7dd0d | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:38:35.008 | 502e999363d14e19b2ecac556be7dd0d | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:38:35.010 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 184.94ms
INFO:     127.0.0.1:52751 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:38:35.038 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:35.038 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:35.412 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.373s
2025-12-23 17:38:35.412 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.3728487491607666
2025-12-23 17:38:35.413 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:35.413 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:35.413 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.494s
2025-12-23 17:38:35.414 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:38:35.421 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:35.421 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:38:35.421 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:38:35.490 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:35.530 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:35.530 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:35.784 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.253s
2025-12-23 17:38:35.784 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.25398707389831543
2025-12-23 17:38:35.784 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:35.785 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:35.785 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.364s
2025-12-23 17:38:35.785 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:38:35.792 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:35.793 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:38:35.793 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:38:35.865 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:35.894 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:35.894 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:36.142 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.247s
2025-12-23 17:38:36.143 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.24829936027526855
2025-12-23 17:38:36.145 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:36.145 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:36.146 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.354s
2025-12-23 17:38:36.146 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:38:36.152 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:36.152 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:38:36.152 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:38:36.249 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:36.290 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:36.290 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:37.208 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.918s
2025-12-23 17:38:37.209 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9191222190856934
2025-12-23 17:38:37.209 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:37.210 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:37.210 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.058s
2025-12-23 17:38:37.210 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:38:37.239 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:37.239 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:38:37.239 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:38:37.305 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:37.343 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:38:37.343 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:37.602 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.259s
2025-12-23 17:38:37.602 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2592332363128662
2025-12-23 17:38:37.603 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:38:37.603 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:37.604 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.365s
2025-12-23 17:38:37.604 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:38:37.611 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:37.615 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:38:37.656 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:38:37.657 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:38:37.658 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:38:37.658 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:38:37.662 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.46秒
2025-12-23 17:38:37.663 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:38:37.792 | 4e4c7a9165f048a2af7ade774e195a02 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
INFO:     127.0.0.1:59366 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:38:37.833 | 4e4c7a9165f048a2af7ade774e195a02 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:38:37.834 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 168.92ms
2025-12-23 17:38:37.838 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:38:38.291 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:38:38.292 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:38:38.292 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:38:38.293 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:38:38.293 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:38:38.293 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:38:38.316 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:38:38.316 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:38:38.316 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:38:38.429 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:38:38.434 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:38:38.462 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:38:38.462 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:38:38.463 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:38:38.523 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:38.551 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:38:38.580 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:38.581 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc2N2JlYTM3LTZkOWMtNDA3ZC1hMjc2LTc0ODBmNGI5YmJmOSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozOSJ9LCJleHAiOjE3NjY1NjkxMjB9.VcMT6_Hfyf7I6BzV0V0oRKO-Duv0yhf8M2MqAS7wdFQ']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc2N2JlYTM3LTZkOWMtNDA3ZC1hMjc2LTc0ODBmNGI5YmJmOSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozOSJ9LCJleHAiOjE3NjY1NjkxMjB9.VcMT6_Hfyf7I6BzV0V0oRKO-Duv0yhf8M2MqAS7wdFQ
2025-12-23 17:38:39.765 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.183s
2025-12-23 17:38:39.765 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.1832756996154785
2025-12-23 17:38:39.766 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
2025-12-23 17:38:39.822 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc2N2JlYTM3LTZkOWMtNDA3ZC1hMjc2LTc0ODBmNGI5YmJmOSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozOSJ9LCJleHAiOjE3NjY1NjkxMjB9.VcMT6_Hfyf7I6BzV0V0oRKO-Duv0yhf8M2MqAS7wdFQ', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc2N2JlYTM3LTZkOWMtNDA3ZC1hMjc2LTc0ODBmNGI5YmJmOSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozOSJ9LCJleHAiOjE3NjY1NjkxMjB9.VcMT6_Hfyf7I6BzV0V0oRKO-Duv0yhf8M2MqAS7wdFQ'}, 'execution_time': 0.05645561218261719, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc2N2JlYTM3LTZkOWMtNDA3ZC1hMjc2LTc0ODBmNGI5YmJmOSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozODozOSJ9LCJleHAiOjE3NjY1NjkxMjB9.VcMT6_Hfyf7I6BzV0V0oRKO-Duv0yhf8M2MqAS7wdFQ'}}
2025-12-23 17:38:39.823 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:38:39.823 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.360s
2025-12-23 17:38:39.823 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:38:39.831 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:39.831 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:38:39.831 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:38:39.831 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:38:39.896 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:39.927 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:39.927 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:40.876 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.948s
2025-12-23 17:38:40.876 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9482884407043457
2025-12-23 17:38:40.877 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:40.877 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:40.878 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.047s
2025-12-23 17:38:40.879 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:38:40.891 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:40.892 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:38:40.892 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:38:40.993 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:41.025 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:41.025 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:41.282 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.256s
2025-12-23 17:38:41.282 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.25615715980529785
2025-12-23 17:38:41.283 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:41.283 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:41.284 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.393s
2025-12-23 17:38:41.284 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:38:41.290 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:41.290 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:38:41.291 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:38:41.359 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:41.392 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:41.392 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:41.789 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.395s
2025-12-23 17:38:41.789 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.39614367485046387
2025-12-23 17:38:41.790 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:41.791 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:41.792 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.502s
2025-12-23 17:38:41.792 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:38:41.804 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:41.804 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:38:41.804 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:38:41.866 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:41.909 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:41.910 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:42.173 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.263s
2025-12-23 17:38:42.173 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.263134241104126
2025-12-23 17:38:42.174 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:38:42.174 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:42.174 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.371s
2025-12-23 17:38:42.174 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:38:42.181 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:38:42.181 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:38:42.182 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:38:42.261 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:38:42.293 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:38:42.294 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:38:44.662 | 9c55e03063c144aba0c3cf1ad2fb9aa6 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:38:44.674 | 9c55e03063c144aba0c3cf1ad2fb9aa6 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:38:44.675 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 1438.90ms
INFO:     127.0.0.1:55917 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:00.689 |  | DEBUG    | config.get_scheduler:try_acquire_lock:269 - [Worker-1510b4b0] 任务锁已被占用: job_id=1, holder=f195f8f5:2025-12-23T17:38:38.152836, TTL=38s
2025-12-23 17:39:00.689 |  | INFO     | config.get_scheduler:async_wrapper:368 - [Worker-1510b4b0] 任务已被其他 Worker 执行，跳过: job_id=1
2025-12-23 17:39:18.525 | d6c0cbbee80a4c1a9067724145ecb62e | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:18.549 | d6c0cbbee80a4c1a9067724145ecb62e | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:18.551 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 192.52ms
INFO:     127.0.0.1:61715 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:18.878 |  | DEBUG    | config.get_scheduler:try_acquire_lock:269 - [Worker-20e69fe9] 任务锁已被占用: job_id=1, holder=f195f8f5:2025-12-23T17:38:38.152836, TTL=19s
2025-12-23 17:39:18.878 |  | INFO     | config.get_scheduler:async_wrapper:368 - [Worker-20e69fe9] 任务已被其他 Worker 执行，跳过: job_id=1
2025-12-23 17:39:18.879 |  | WARNING  | config.get_scheduler:scheduler_event_listener:699 - [Scheduler] 任务延迟执行: job_id=1, 计划时间=17:39:00, 实际时间=17:39:18, 延迟=18.9秒
2025-12-23 17:39:19.326 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 37.032s
2025-12-23 17:39:19.326 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时37.031551361083984
2025-12-23 17:39:19.327 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:19.327 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:19.327 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 37.144s
Execution of job "执行工作流3 (trigger: cron[month='*', day='*', hour='*', minute='0/1', second='0'], next run at: 2025-12-23 17:39:00 CST)" skipped: maximum number of running instances reached (1)
2025-12-23 17:39:19.328 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:19.399 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:19.399 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:19.399 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:39:19.524 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:19.555 | f0eef16da2c2438889d1b3bb84378e4e | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:19.560 | f0eef16da2c2438889d1b3bb84378e4e | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:19.562 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 170.31ms
INFO:     127.0.0.1:52840 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:19.589 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:19.589 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:20.329 | 221c1b6e394048a9a69135e6b35544be | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:20.335 | 221c1b6e394048a9a69135e6b35544be | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:20.337 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 122.79ms
INFO:     127.0.0.1:52845 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:20.695 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.106s
2025-12-23 17:39:20.695 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.1063897609710693
2025-12-23 17:39:20.696 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:20.697 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:20.698 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.299s
2025-12-23 17:39:20.699 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:20.709 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:20.710 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:20.710 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:39:20.792 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:20.825 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:39:20.825 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:20.994 | 2e29547b8b154e36a7ddce53422c5c48 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:21.000 | 2e29547b8b154e36a7ddce53422c5c48 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:21.002 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 165.92ms
INFO:     127.0.0.1:52849 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:21.127 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.302s
2025-12-23 17:39:21.127 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.3021409511566162
2025-12-23 17:39:21.128 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:39:21.128 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:21.128 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.417s
2025-12-23 17:39:21.128 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:21.134 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:21.138 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:39:21.181 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:39:21.181 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:39:21.184 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:39:21.184 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:39:21.187 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时42.85秒
2025-12-23 17:39:21.187 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:39:21.322 | 27049bf33b944476819ab6b7f8ccd379 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
2025-12-23 17:39:21.361 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
INFO:     127.0.0.1:52852 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:39:21.396 | 27049bf33b944476819ab6b7f8ccd379 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:39:21.398 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 208.48ms
2025-12-23 17:39:21.570 | daf6ad7e35734dd697c5a5107d61e70f | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:21.576 | daf6ad7e35734dd697c5a5107d61e70f | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:21.577 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 119.47ms
INFO:     127.0.0.1:50699 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:21.799 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:39:21.799 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:39:21.801 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:39:21.801 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:39:21.801 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:39:21.801 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:39:21.821 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:39:21.822 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:39:21.822 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:39:21.977 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:39:21.981 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:39:22.017 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:39:22.017 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:22.018 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:39:22.097 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:22.129 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:39:22.163 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:22.163 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:23.031 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.868s
2025-12-23 17:39:23.032 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.8690001964569092
2025-12-23 17:39:23.033 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc1ZDI5MzA4LWVlNTgtNDU3Yy1iYWEyLTRmNTc5Y2I4MmNhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyMyJ9LCJleHAiOjE3NjY1NjkxNjN9.X4RGynxrJ_wksBHVeIbuAArCqgruW8XpSPUN5Bj30oI']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc1ZDI5MzA4LWVlNTgtNDU3Yy1iYWEyLTRmNTc5Y2I4MmNhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyMyJ9LCJleHAiOjE3NjY1NjkxNjN9.X4RGynxrJ_wksBHVeIbuAArCqgruW8XpSPUN5Bj30oI
2025-12-23 17:39:23.088 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc1ZDI5MzA4LWVlNTgtNDU3Yy1iYWEyLTRmNTc5Y2I4MmNhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyMyJ9LCJleHAiOjE3NjY1NjkxNjN9.X4RGynxrJ_wksBHVeIbuAArCqgruW8XpSPUN5Bj30oI', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc1ZDI5MzA4LWVlNTgtNDU3Yy1iYWEyLTRmNTc5Y2I4MmNhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyMyJ9LCJleHAiOjE3NjY1NjkxNjN9.X4RGynxrJ_wksBHVeIbuAArCqgruW8XpSPUN5Bj30oI'}, 'execution_time': 0.05479001998901367, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6Ijc1ZDI5MzA4LWVlNTgtNDU3Yy1iYWEyLTRmNTc5Y2I4MmNhZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyMyJ9LCJleHAiOjE3NjY1NjkxNjN9.X4RGynxrJ_wksBHVeIbuAArCqgruW8XpSPUN5Bj30oI'}}
2025-12-23 17:39:23.088 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:39:23.088 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.070s
2025-12-23 17:39:23.089 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:23.096 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:23.097 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:39:23.097 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:23.097 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:39:23.163 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:23.193 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:23.193 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:24.115 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.921s
2025-12-23 17:39:24.115 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9220504760742188
2025-12-23 17:39:24.116 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:24.116 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:24.116 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.019s
2025-12-23 17:39:24.116 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:24.125 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:24.126 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:24.127 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:39:24.192 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:24.222 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:24.222 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:24.457 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.235s
2025-12-23 17:39:24.457 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.23515987396240234
2025-12-23 17:39:24.457 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:24.458 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:24.458 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.332s
2025-12-23 17:39:24.458 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:24.463 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:24.463 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:24.464 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:39:24.539 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:24.567 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:24.568 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:24.924 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.354s
2025-12-23 17:39:24.925 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.35536956787109375
2025-12-23 17:39:24.926 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:24.927 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:24.927 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.462s
2025-12-23 17:39:24.928 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:24.936 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:24.936 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:24.937 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:39:24.997 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:25.027 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:25.028 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:25.274 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.246s
2025-12-23 17:39:25.275 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.24692916870117188
2025-12-23 17:39:25.275 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:25.276 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:25.276 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.339s
2025-12-23 17:39:25.276 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:25.283 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:25.283 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:25.283 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:39:25.389 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:25.418 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:25.418 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:25.706 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.288s
2025-12-23 17:39:25.706 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2885298728942871
2025-12-23 17:39:25.707 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:25.707 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:25.707 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.424s
2025-12-23 17:39:25.707 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:25.717 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:25.717 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:25.717 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:39:25.833 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:25.874 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:25.874 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:26.612 | 55fb2e85657540bbadfd1505cc6f99ba | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:26.617 | 55fb2e85657540bbadfd1505cc6f99ba | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:26.619 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 122.84ms
INFO:     127.0.0.1:56931 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:26.809 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.934s
2025-12-23 17:39:26.810 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9363243579864502
2025-12-23 17:39:26.810 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:26.810 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:26.811 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.094s
2025-12-23 17:39:26.811 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:26.824 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:26.824 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:26.824 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:39:26.898 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:26.929 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:39:26.929 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:27.189 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.258s
2025-12-23 17:39:27.190 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2591094970703125
2025-12-23 17:39:27.190 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:39:27.190 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:27.190 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.366s
2025-12-23 17:39:27.190 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:27.199 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:27.204 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:39:27.247 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:39:27.247 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:39:27.251 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.40秒
2025-12-23 17:39:27.252 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:39:27.424 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:39:27.843 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:39:27.845 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:39:27.845 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:39:27.845 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:39:27.846 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:39:27.846 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:39:27.867 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:39:27.867 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:39:27.868 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:39:27.982 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:39:27.986 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:39:28.026 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:39:28.026 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:28.026 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:39:28.104 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:28.135 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:39:28.475 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:28.476 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:29.336 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.859s
2025-12-23 17:39:29.336 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.859445333480835
2025-12-23 17:39:29.336 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjczYmJmZGZhLWQ4MDQtNDdlZS1iYjU2LTgwNGJjYTZkOGExMiIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyOSJ9LCJleHAiOjE3NjY1NjkxNzB9.f9Ab0tKYfNa4RxU0slkzc33nypvPb_EqYgq4jHwntVg']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjczYmJmZGZhLWQ4MDQtNDdlZS1iYjU2LTgwNGJjYTZkOGExMiIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyOSJ9LCJleHAiOjE3NjY1NjkxNzB9.f9Ab0tKYfNa4RxU0slkzc33nypvPb_EqYgq4jHwntVg
2025-12-23 17:39:29.399 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjczYmJmZGZhLWQ4MDQtNDdlZS1iYjU2LTgwNGJjYTZkOGExMiIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyOSJ9LCJleHAiOjE3NjY1NjkxNzB9.f9Ab0tKYfNa4RxU0slkzc33nypvPb_EqYgq4jHwntVg', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjczYmJmZGZhLWQ4MDQtNDdlZS1iYjU2LTgwNGJjYTZkOGExMiIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyOSJ9LCJleHAiOjE3NjY1NjkxNzB9.f9Ab0tKYfNa4RxU0slkzc33nypvPb_EqYgq4jHwntVg'}, 'execution_time': 0.06078600883483887, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjczYmJmZGZhLWQ4MDQtNDdlZS1iYjU2LTgwNGJjYTZkOGExMiIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOToyOSJ9LCJleHAiOjE3NjY1NjkxNzB9.f9Ab0tKYfNa4RxU0slkzc33nypvPb_EqYgq4jHwntVg'}}
2025-12-23 17:39:29.399 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:39:29.399 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.373s
2025-12-23 17:39:29.399 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:29.406 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:29.406 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:39:29.407 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:29.407 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:39:29.481 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:29.510 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:29.511 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:30.411 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.900s
2025-12-23 17:39:30.412 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9008264541625977
2025-12-23 17:39:30.412 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:30.413 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:30.413 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.007s
2025-12-23 17:39:30.414 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:30.422 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:30.423 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:30.423 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:39:30.532 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:30.557 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:30.557 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:30.807 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.249s
2025-12-23 17:39:30.808 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.24964284896850586
2025-12-23 17:39:30.808 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:30.808 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:30.809 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.385s
2025-12-23 17:39:30.809 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:30.814 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:30.814 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:30.814 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:39:30.877 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:30.911 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:30.911 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:31.247 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.336s
2025-12-23 17:39:31.247 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.3358800411224365
2025-12-23 17:39:31.248 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:31.248 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:31.248 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.434s
2025-12-23 17:39:31.248 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:31.258 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:31.258 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:31.258 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:39:31.361 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:31.388 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:31.388 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:31.650 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.262s
2025-12-23 17:39:31.652 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2635054588317871
2025-12-23 17:39:31.653 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:31.653 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:31.654 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.395s
2025-12-23 17:39:31.654 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:31.663 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:31.663 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:31.663 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:39:31.730 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:31.757 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:31.757 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:32.035 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.278s
2025-12-23 17:39:32.035 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.27808260917663574
2025-12-23 17:39:32.035 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:32.036 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:32.036 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.373s
2025-12-23 17:39:32.036 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:32.041 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:32.041 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:32.043 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:39:32.136 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:32.171 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:32.172 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:33.255 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.083s
2025-12-23 17:39:33.255 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0831398963928223
2025-12-23 17:39:33.255 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:33.256 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:33.256 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.214s
2025-12-23 17:39:33.256 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:33.265 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:33.265 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:33.265 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:39:33.344 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:33.374 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:39:33.374 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:33.649 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.275s
2025-12-23 17:39:33.649 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.27480125427246094
2025-12-23 17:39:33.649 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:39:33.649 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:33.649 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.384s
2025-12-23 17:39:33.651 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:33.656 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:33.661 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:39:33.704 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:39:33.706 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:39:33.710 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.82秒
2025-12-23 17:39:33.711 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:39:33.882 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:39:34.319 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:39:34.322 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:39:34.322 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:39:34.322 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:39:34.323 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:39:34.323 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:39:34.342 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:39:34.343 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:39:34.343 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:39:34.454 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:39:34.460 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:39:34.487 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:39:34.487 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:34.487 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:39:34.550 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:34.580 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:39:34.608 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:34.608 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:35.300 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:39:35.300 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:39:35.301 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:39:35.301 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:39:35.424 | db9095ca6b5e42ae8ee0d19f2164dcbc | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:query_detail_report_api_workflow_report:104 - id:<built-in function id>
INFO:     127.0.0.1:55926 - "GET /report/api_workflow_report/4181 HTTP/1.1" 200 OK
2025-12-23 17:39:35.437 | db9095ca6b5e42ae8ee0d19f2164dcbc | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:query_detail_report_api_workflow_report:107 - 获取report_id为4181的信息成功
2025-12-23 17:39:35.439 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/4181 - 200 - 137.22ms
2025-12-23 17:39:35.506 | bfb53d8dc396433bbe3652c012650ab3 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
2025-12-23 17:39:35.532 | 4e676b81ee6a41c8bac5d1c13c4efc1a | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
2025-12-23 17:39:35.551 | bfb53d8dc396433bbe3652c012650ab3 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:39:35.553 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 244.62ms
INFO:     127.0.0.1:58440 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:39:35.572 | 4e676b81ee6a41c8bac5d1c13c4efc1a | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:39:35.573 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 259.53ms
INFO:     127.0.0.1:59342 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:39:35.685 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.077s
2025-12-23 17:39:35.686 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0780510902404785
2025-12-23 17:39:35.686 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImQwMTc3NTFlLTczYzgtNDM1ZS04ODYzLWViZmFlOGM0MTBkOCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTozNSJ9LCJleHAiOjE3NjY1NjkxNzZ9.czgKeflKaH_0JvFpF_Rrm4ibSsGsqzBt3CQIchboQRM']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImQwMTc3NTFlLTczYzgtNDM1ZS04ODYzLWViZmFlOGM0MTBkOCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTozNSJ9LCJleHAiOjE3NjY1NjkxNzZ9.czgKeflKaH_0JvFpF_Rrm4ibSsGsqzBt3CQIchboQRM
2025-12-23 17:39:35.743 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImQwMTc3NTFlLTczYzgtNDM1ZS04ODYzLWViZmFlOGM0MTBkOCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTozNSJ9LCJleHAiOjE3NjY1NjkxNzZ9.czgKeflKaH_0JvFpF_Rrm4ibSsGsqzBt3CQIchboQRM', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImQwMTc3NTFlLTczYzgtNDM1ZS04ODYzLWViZmFlOGM0MTBkOCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTozNSJ9LCJleHAiOjE3NjY1NjkxNzZ9.czgKeflKaH_0JvFpF_Rrm4ibSsGsqzBt3CQIchboQRM'}, 'execution_time': 0.055815696716308594, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImQwMTc3NTFlLTczYzgtNDM1ZS04ODYzLWViZmFlOGM0MTBkOCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTozNSJ9LCJleHAiOjE3NjY1NjkxNzZ9.czgKeflKaH_0JvFpF_Rrm4ibSsGsqzBt3CQIchboQRM'}}
2025-12-23 17:39:35.743 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:39:35.744 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.257s
2025-12-23 17:39:35.744 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:35.753 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:35.754 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:39:35.754 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:35.754 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:39:35.906 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:35.938 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:35.939 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:36.894 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.955s
2025-12-23 17:39:36.894 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.955634355545044
2025-12-23 17:39:36.894 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:36.895 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:36.895 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.141s
2025-12-23 17:39:36.895 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:36.906 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:36.907 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:36.907 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:39:36.971 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:36.999 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:36.999 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:37.238 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.239s
2025-12-23 17:39:37.238 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.23895263671875
2025-12-23 17:39:37.238 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:37.238 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:37.239 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.332s
2025-12-23 17:39:37.239 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:37.244 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:37.244 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:37.245 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:39:37.307 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:37.333 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:37.333 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:37.679 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.345s
2025-12-23 17:39:37.680 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.34640026092529297
2025-12-23 17:39:37.680 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:37.680 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:37.680 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.434s
2025-12-23 17:39:37.681 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:37.689 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:37.689 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:37.690 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:39:37.765 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:37.793 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:37.794 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:38.040 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.246s
2025-12-23 17:39:38.041 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.24686312675476074
2025-12-23 17:39:38.041 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:38.042 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:38.042 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.351s
2025-12-23 17:39:38.042 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:38.052 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:38.052 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:38.052 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:39:38.153 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:38.183 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:38.184 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:38.434 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.250s
2025-12-23 17:39:38.435 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2510988712310791
2025-12-23 17:39:38.435 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:38.436 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:38.436 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.383s
2025-12-23 17:39:38.436 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:38.444 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:38.445 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:38.445 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:39:38.565 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:38.601 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:38.601 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:39.611 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.010s
2025-12-23 17:39:39.612 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0110371112823486
2025-12-23 17:39:39.612 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:39.612 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:39.612 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.167s
2025-12-23 17:39:39.612 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:39.620 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:39.621 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:39.621 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:39:39.698 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:39.730 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:39:39.731 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:39.999 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.268s
2025-12-23 17:39:39.999 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2682921886444092
2025-12-23 17:39:39.999 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:39:39.999 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:40.001 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.379s
2025-12-23 17:39:40.002 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:40.006 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:40.011 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:39:40.050 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:39:40.051 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:39:40.051 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:39:40.051 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:39:40.055 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.69秒
2025-12-23 17:39:40.055 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:39:40.176 | 32cbc14a22ef4fe8b64d216e3f19c1c5 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
2025-12-23 17:39:40.209 | 32cbc14a22ef4fe8b64d216e3f19c1c5 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:39:40.211 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 149.33ms
INFO:     127.0.0.1:62634 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:39:42.704 | 06ff36aab9a34d83b2fce4ae57c78a86 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:42.707 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:39:42.709 | 06ff36aab9a34d83b2fce4ae57c78a86 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:42.711 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 127.83ms
INFO:     127.0.0.1:53693 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:43.159 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:39:43.161 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:39:43.161 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:39:43.162 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:39:43.162 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:39:43.162 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:39:43.182 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:39:43.183 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:39:43.183 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:39:43.289 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:39:43.293 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:39:43.325 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:39:43.325 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:43.325 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:39:43.395 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:43.423 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:39:43.452 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:43.452 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:43.784 | d77e76b6952746cb9600589f22378e60 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:43.790 | d77e76b6952746cb9600589f22378e60 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:43.791 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 125.95ms
INFO:     127.0.0.1:53700 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:44.336 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.883s
2025-12-23 17:39:44.336 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.8825235366821289
2025-12-23 17:39:44.337 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjRmNmZjZWRkLTY2MmEtNGYyYS05NTg0LTEwOTNhZDRkMTAzNCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo0NCJ9LCJleHAiOjE3NjY1NjkxODV9.P-4vBuzrT5mqcH3PtjGjRdubr19I9Fz5bPOTrboZB70']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjRmNmZjZWRkLTY2MmEtNGYyYS05NTg0LTEwOTNhZDRkMTAzNCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo0NCJ9LCJleHAiOjE3NjY1NjkxODV9.P-4vBuzrT5mqcH3PtjGjRdubr19I9Fz5bPOTrboZB70
2025-12-23 17:39:44.404 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjRmNmZjZWRkLTY2MmEtNGYyYS05NTg0LTEwOTNhZDRkMTAzNCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo0NCJ9LCJleHAiOjE3NjY1NjkxODV9.P-4vBuzrT5mqcH3PtjGjRdubr19I9Fz5bPOTrboZB70', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjRmNmZjZWRkLTY2MmEtNGYyYS05NTg0LTEwOTNhZDRkMTAzNCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo0NCJ9LCJleHAiOjE3NjY1NjkxODV9.P-4vBuzrT5mqcH3PtjGjRdubr19I9Fz5bPOTrboZB70'}, 'execution_time': 0.06552457809448242, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjRmNmZjZWRkLTY2MmEtNGYyYS05NTg0LTEwOTNhZDRkMTAzNCIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo0NCJ9LCJleHAiOjE3NjY1NjkxODV9.P-4vBuzrT5mqcH3PtjGjRdubr19I9Fz5bPOTrboZB70'}}
2025-12-23 17:39:44.405 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:39:44.405 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.079s
2025-12-23 17:39:44.406 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:44.413 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:44.414 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:39:44.414 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:44.414 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:39:44.542 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:44.571 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:44.571 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:45.524 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.952s
2025-12-23 17:39:45.524 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9518542289733887
2025-12-23 17:39:45.525 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:45.525 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:45.525 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.111s
2025-12-23 17:39:45.525 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:45.536 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:45.536 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:45.537 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:39:45.599 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:45.627 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:45.628 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:45.860 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.233s
2025-12-23 17:39:45.861 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2336409091949463
2025-12-23 17:39:45.861 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:45.861 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:45.863 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.325s
2025-12-23 17:39:45.863 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:45.872 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:45.872 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:45.872 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:39:45.953 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:45.978 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:45.978 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:46.308 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.329s
2025-12-23 17:39:46.308 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.33051133155822754
2025-12-23 17:39:46.309 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:46.309 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:46.309 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.436s
2025-12-23 17:39:46.310 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:46.315 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:46.316 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:46.316 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:39:46.397 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:46.422 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:46.423 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:46.693 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.270s
2025-12-23 17:39:46.693 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.26979756355285645
2025-12-23 17:39:46.693 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:46.694 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:46.694 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.378s
2025-12-23 17:39:46.694 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:46.702 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:46.702 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:46.702 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:39:46.808 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:46.842 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:46.842 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:47.108 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.265s
2025-12-23 17:39:47.108 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2660226821899414
2025-12-23 17:39:47.109 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:47.109 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:47.109 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.407s
2025-12-23 17:39:47.109 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:47.115 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:47.115 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:47.116 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:39:47.220 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:47.258 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:47.258 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:47.418 | 699d6f1fe2764f008cbb621552483a83 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:33 - {'report_id': None, 'workflow_id': 1, 'name': None, 'start_time': None, 'end_time': None, 'total_cases': None, 'success_cases': None, 'failed_cases': None, 'duration': None, 'is_success': None, 'report_data': None, 'trigger_type': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 10}
2025-12-23 17:39:47.424 | 699d6f1fe2764f008cbb621552483a83 | INFO     | module_admin.api_workflow.api_workflow_report.controller.api_workflow_report_controller:get_report_api_workflow_report_list:37 - 获取成功
2025-12-23 17:39:47.426 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /report/api_workflow_report/list - 200 - 136.15ms
INFO:     127.0.0.1:60084 - "GET /report/api_workflow_report/list?pageNum=1&pageSize=10&workflowId=1 HTTP/1.1" 200 OK
2025-12-23 17:39:48.320 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.061s
2025-12-23 17:39:48.320 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0609958171844482
2025-12-23 17:39:48.320 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:48.320 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:48.321 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.205s
2025-12-23 17:39:48.322 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:48.328 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:48.328 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:48.328 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:39:48.415 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:48.446 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:39:48.447 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:48.721 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.274s
2025-12-23 17:39:48.721 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2744755744934082
2025-12-23 17:39:48.723 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:39:48.723 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:48.723 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.395s
2025-12-23 17:39:48.723 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:48.734 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:48.739 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:39:48.783 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:39:48.784 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:39:48.784 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:39:48.784 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:39:48.789 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.58秒
2025-12-23 17:39:48.789 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:39:48.956 | 49453cf6ab1248b4a6c22aa56d5ac07d | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
2025-12-23 17:39:48.991 | 49453cf6ab1248b4a6c22aa56d5ac07d | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:39:48.991 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:39:48.992 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 199.96ms
INFO:     127.0.0.1:58311 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:39:49.444 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:39:49.445 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:39:49.445 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:39:49.445 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:39:49.446 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:39:49.446 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:39:49.469 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:39:49.469 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:39:49.469 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:39:49.591 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:39:49.594 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:39:49.639 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:39:49.639 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:49.639 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:39:49.733 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:49.793 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:39:49.826 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:49.826 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:50.761 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.936s
2025-12-23 17:39:50.762 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9362967014312744
2025-12-23 17:39:50.762 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImY5NDE0NzdhLTliOTQtNGY1Ny05ZTQ2LWE2MTI0ZjgzMTFiMSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1MCJ9LCJleHAiOjE3NjY1NjkxOTF9.hC-7pU58bPmQbBxjZNCy_5pccQFcr3Su5hfe9QFjc8Y']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImY5NDE0NzdhLTliOTQtNGY1Ny05ZTQ2LWE2MTI0ZjgzMTFiMSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1MCJ9LCJleHAiOjE3NjY1NjkxOTF9.hC-7pU58bPmQbBxjZNCy_5pccQFcr3Su5hfe9QFjc8Y
2025-12-23 17:39:50.816 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImY5NDE0NzdhLTliOTQtNGY1Ny05ZTQ2LWE2MTI0ZjgzMTFiMSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1MCJ9LCJleHAiOjE3NjY1NjkxOTF9.hC-7pU58bPmQbBxjZNCy_5pccQFcr3Su5hfe9QFjc8Y', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImY5NDE0NzdhLTliOTQtNGY1Ny05ZTQ2LWE2MTI0ZjgzMTFiMSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1MCJ9LCJleHAiOjE3NjY1NjkxOTF9.hC-7pU58bPmQbBxjZNCy_5pccQFcr3Su5hfe9QFjc8Y'}, 'execution_time': 0.05403494834899902, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImY5NDE0NzdhLTliOTQtNGY1Ny05ZTQ2LWE2MTI0ZjgzMTFiMSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1MCJ9LCJleHAiOjE3NjY1NjkxOTF9.hC-7pU58bPmQbBxjZNCy_5pccQFcr3Su5hfe9QFjc8Y'}}
2025-12-23 17:39:50.816 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:39:50.817 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.178s
2025-12-23 17:39:50.818 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:50.824 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:50.824 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:39:50.824 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:50.824 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:39:50.925 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:50.956 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:50.956 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:51.973 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.017s
2025-12-23 17:39:51.974 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0179481506347656
2025-12-23 17:39:51.974 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:51.975 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:51.975 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.151s
2025-12-23 17:39:51.975 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:51.983 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:51.983 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:51.984 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:39:52.051 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:52.092 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:52.093 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:52.340 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.247s
2025-12-23 17:39:52.340 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2471299171447754
2025-12-23 17:39:52.341 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:52.342 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:52.342 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.357s
2025-12-23 17:39:52.342 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:52.347 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:52.347 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:52.347 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:39:52.410 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:52.448 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:52.449 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:52.825 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.376s
2025-12-23 17:39:52.826 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.37690043449401855
2025-12-23 17:39:52.827 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:52.827 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:52.828 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.481s
2025-12-23 17:39:52.828 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:52.840 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:52.840 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:52.841 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:39:52.904 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:52.940 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:52.941 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:53.197 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.257s
2025-12-23 17:39:53.198 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2576017379760742
2025-12-23 17:39:53.199 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:53.199 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:53.199 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.359s
2025-12-23 17:39:53.201 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:53.207 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:53.207 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:53.208 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:39:53.274 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:53.307 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:53.307 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:53.598 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.289s
2025-12-23 17:39:53.599 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.29138660430908203
2025-12-23 17:39:53.599 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:53.600 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:53.600 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.391s
2025-12-23 17:39:53.601 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:53.607 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:53.607 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:53.608 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:39:53.714 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:53.750 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:53.750 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:54.666 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.916s
2025-12-23 17:39:54.667 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9165384769439697
2025-12-23 17:39:54.667 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:54.668 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:54.668 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.060s
2025-12-23 17:39:54.668 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:54.680 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:54.680 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:54.680 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:39:54.784 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:54.849 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:39:54.849 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:55.119 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.270s
2025-12-23 17:39:55.119 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.27048301696777344
2025-12-23 17:39:55.119 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:39:55.119 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:55.119 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.440s
2025-12-23 17:39:55.119 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:39:55.125 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:55.129 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:39:55.169 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:39:55.169 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:39:55.169 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:39:55.169 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:39:55.174 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.68秒
2025-12-23 17:39:55.175 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:39:55.308 | b5334746db3242c2af9dc29a8e767e5b | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
INFO:     127.0.0.1:60779 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:39:55.341 | b5334746db3242c2af9dc29a8e767e5b | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:39:55.342 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 165.15ms
2025-12-23 17:39:55.365 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:39:55.779 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:39:55.780 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:39:55.781 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:39:55.781 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:39:55.783 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:39:55.783 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:39:55.803 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:39:55.803 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:39:55.803 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:39:55.923 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:39:55.928 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:39:55.956 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:39:55.957 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:55.957 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:39:56.022 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:56.059 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:39:56.092 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:56.093 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImEzYjkzMTBjLTg1YmQtNGZhOS1iMDMyLTY2ZWE0MTI3ZjIwZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1NyJ9LCJleHAiOjE3NjY1NjkxOTd9.69QVwoatDx13cix6Vd2b7cvFuvYn0vW8KTgroL_e_bM']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImEzYjkzMTBjLTg1YmQtNGZhOS1iMDMyLTY2ZWE0MTI3ZjIwZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1NyJ9LCJleHAiOjE3NjY1NjkxOTd9.69QVwoatDx13cix6Vd2b7cvFuvYn0vW8KTgroL_e_bM
2025-12-23 17:39:57.067 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.974s
2025-12-23 17:39:57.067 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.973872184753418
2025-12-23 17:39:57.067 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
2025-12-23 17:39:57.124 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImEzYjkzMTBjLTg1YmQtNGZhOS1iMDMyLTY2ZWE0MTI3ZjIwZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1NyJ9LCJleHAiOjE3NjY1NjkxOTd9.69QVwoatDx13cix6Vd2b7cvFuvYn0vW8KTgroL_e_bM', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImEzYjkzMTBjLTg1YmQtNGZhOS1iMDMyLTY2ZWE0MTI3ZjIwZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1NyJ9LCJleHAiOjE3NjY1NjkxOTd9.69QVwoatDx13cix6Vd2b7cvFuvYn0vW8KTgroL_e_bM'}, 'execution_time': 0.05517911911010742, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImEzYjkzMTBjLTg1YmQtNGZhOS1iMDMyLTY2ZWE0MTI3ZjIwZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzozOTo1NyJ9LCJleHAiOjE3NjY1NjkxOTd9.69QVwoatDx13cix6Vd2b7cvFuvYn0vW8KTgroL_e_bM'}}
2025-12-23 17:39:57.124 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:39:57.125 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.167s
2025-12-23 17:39:57.125 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:39:57.135 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:57.135 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:39:57.135 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:57.135 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:39:57.229 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:57.261 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:57.261 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:58.231 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.969s
2025-12-23 17:39:58.231 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9690220355987549
2025-12-23 17:39:58.231 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:58.231 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:58.231 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.097s
2025-12-23 17:39:58.231 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:39:58.239 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:58.239 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:58.239 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:39:58.302 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:58.332 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:58.332 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:58.578 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.247s
2025-12-23 17:39:58.579 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.24761295318603516
2025-12-23 17:39:58.579 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:58.579 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:58.579 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.340s
2025-12-23 17:39:58.580 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:39:58.585 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:58.586 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:58.586 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:39:58.651 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:58.677 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:58.677 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:59.043 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.365s
2025-12-23 17:39:59.044 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.3663475513458252
2025-12-23 17:39:59.044 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:59.045 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:59.045 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.459s
2025-12-23 17:39:59.045 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:39:59.051 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:59.051 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:59.051 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:39:59.122 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:59.150 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:59.150 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:59.431 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.280s
2025-12-23 17:39:59.432 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.28104662895202637
2025-12-23 17:39:59.432 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:59.433 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:59.433 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.382s
2025-12-23 17:39:59.433 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:39:59.439 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:59.440 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:59.440 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:39:59.517 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:59.551 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:59.552 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:59.857 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.305s
2025-12-23 17:39:59.857 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.3053007125854492
2025-12-23 17:39:59.858 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:39:59.858 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:39:59.858 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.418s
2025-12-23 17:39:59.858 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:39:59.865 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:39:59.865 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:39:59.865 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:39:59.957 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:39:59.993 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:39:59.993 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
Execution of job "执行工作流3 (trigger: cron[month='*', day='*', hour='*', minute='0/1', second='0'], next run at: 2025-12-23 17:40:00 CST)" skipped: maximum number of running instances reached (1)
2025-12-23 17:40:00.554 |  | DEBUG    | config.get_scheduler:try_acquire_lock:269 - [Worker-20e69fe9] 任务锁已被占用: job_id=1, holder=f195f8f5:2025-12-23T17:39:55.635088, TTL=55s
2025-12-23 17:40:00.555 |  | INFO     | config.get_scheduler:async_wrapper:368 - [Worker-20e69fe9] 任务已被其他 Worker 执行，跳过: job_id=1
2025-12-23 17:40:00.581 |  | DEBUG    | config.get_scheduler:try_acquire_lock:269 - [Worker-1510b4b0] 任务锁已被占用: job_id=1, holder=f195f8f5:2025-12-23T17:39:55.635088, TTL=55s
2025-12-23 17:40:00.582 |  | INFO     | config.get_scheduler:async_wrapper:368 - [Worker-1510b4b0] 任务已被其他 Worker 执行，跳过: job_id=1
2025-12-23 17:40:01.042 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.049s
2025-12-23 17:40:01.042 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.0491828918457031
2025-12-23 17:40:01.042 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:40:01.042 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:01.044 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.178s
2025-12-23 17:40:01.044 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:40:01.051 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:01.051 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:40:01.052 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:40:01.165 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:01.203 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:40:01.204 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:01.494 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.291s
2025-12-23 17:40:01.495 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2914900779724121
2025-12-23 17:40:01.496 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:40:01.496 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:01.497 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.445s
2025-12-23 17:40:01.498 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:40:01.505 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:01.509 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:40:01.555 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:40:01.555 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:40:01.555 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:40:01.555 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:40:01.559 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.73秒
2025-12-23 17:40:01.560 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:40:01.691 | 97032f582c5f462991b50bee321281ed | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
INFO:     127.0.0.1:64573 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:40:01.727 | 97032f582c5f462991b50bee321281ed | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:40:01.728 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 164.03ms
2025-12-23 17:40:01.753 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:40:02.241 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:40:02.244 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17:40:02.244 |  | DEBUG    | config.get_scheduler:async_wrapper:373 - [Worker-f195f8f5] 准备调用任务函数...
2025-12-23 17:40:02.245 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:144 - [execute_workflow_sync] 开始执行，workflow_id=1
2025-12-23 17:40:02.245 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:155 - [execute_workflow_sync] 准备获取数据库连接...
2025-12-23 17:40:02.246 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:157 - [execute_workflow_sync] 数据库连接成功，准备获取 HTTP client...
2025-12-23 17:40:02.267 |  | INFO     | config.get_httpclient:get_http_client:77 - 获取http_client
2025-12-23 17:40:02.267 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:159 - [execute_workflow_sync] HTTP client 获取成功，准备创建 Redis 连接...
2025-12-23 17:40:02.267 |  | INFO     | config.get_redis:create_redis_pool:109 - 开始连接 Redis...
2025-12-23 17:40:02.406 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:161 - [execute_workflow_sync] Redis 连接成功，准备查询工作流信息...
2025-12-23 17:40:02.411 |  | DEBUG    | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:164 - [execute_workflow_sync] 工作流信息获取成功: 测试套件1
2025-12-23 17:40:02.441 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 开始执行工作流: 测试套件1
2025-12-23 17:40:02.441 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:40:02.441 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2499
2025-12-23 17:40:02.549 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:02.596 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:最大单词数量
2025-12-23 17:40:02.629 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:40:02.629 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
[JSONPath 提取]
  表达式: $.token
  源数据类型: <class 'dict'>
  源数据键: ['code', 'msg', 'token', 'success', 'time']
  提取结果: ['eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImJmMThjMDlmLTMwZWMtNDNjMS1hZjRjLTRjODdkNGYxMThhNSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzo0MDowMyJ9LCJleHAiOjE3NjY1NjkyMDR9.-qzzAEvtwIJzWa-GoNnG64oKnGNiRgQcP7tkk_Hchsc']
  结果类型: <class 'list'>
  最终值: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImJmMThjMDlmLTMwZWMtNDNjMS1hZjRjLTRjODdkNGYxMThhNSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzo0MDowMyJ9LCJleHAiOjE3NjY1NjkyMDR9.-qzzAEvtwIJzWa-GoNnG64oKnGNiRgQcP7tkk_Hchsc
2025-12-23 17:40:03.706 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 1.075s
2025-12-23 17:40:03.707 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时1.076244831085205
2025-12-23 17:40:03.707 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共1个
2025-12-23 17:40:03.768 |  | INFO     | utils.api_tools.executors.manager:_execute_list:77 - teardown_type 脚本执行成功: : 结果：{'success': True, 'message': '变量 token 提取成功，值为: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImJmMThjMDlmLTMwZWMtNDNjMS1hZjRjLTRjODdkNGYxMThhNSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzo0MDowMyJ9LCJleHAiOjE3NjY1NjkyMDR9.-qzzAEvtwIJzWa-GoNnG64oKnGNiRgQcP7tkk_Hchsc', 'data': None, 'error': None, 'variables': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImJmMThjMDlmLTMwZWMtNDNjMS1hZjRjLTRjODdkNGYxMThhNSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzo0MDowMyJ9LCJleHAiOjE3NjY1NjkyMDR9.-qzzAEvtwIJzWa-GoNnG64oKnGNiRgQcP7tkk_Hchsc'}, 'execution_time': 0.061043500900268555, 'log': {'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImJmMThjMDlmLTMwZWMtNDNjMS1hZjRjLTRjODdkNGYxMThhNSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTgwLjExMC4xNDAuNTYiLCJsb2dpbkxvY2F0aW9uIjoiXHU2YzVmXHU4MmNmXHU3NzAxLVx1NTM1N1x1NGVhY1x1NWUwMi1cdTVlZmFcdTkwYmEiLCJicm93c2VyIjoiUHl0aG9uIGFpb2h0dHAgMy4xMi4xNSIsIm9zIjoiT3RoZXIgIiwibG9naW5UaW1lIjoiMjAyNS0xMi0yMyAxNzo0MDowMyJ9LCJleHAiOjE3NjY1NjkyMDR9.-qzzAEvtwIJzWa-GoNnG64oKnGNiRgQcP7tkk_Hchsc'}}
2025-12-23 17:40:03.769 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 1, 失败: 0
2025-12-23 17:40:03.769 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2499，耗时: 1.328s
2025-12-23 17:40:03.770 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Login111111
2025-12-23 17:40:03.776 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:03.776 |  | INFO     | utils.api_workflow_tools.api_workflows_exectors:execute_node_logic:727 - 开始执行Group节点: 分组类别111
2025-12-23 17:40:03.776 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:40:03.776 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2500
2025-12-23 17:40:03.852 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:03.892 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:40:03.892 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:04.784 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.890s
2025-12-23 17:40:04.785 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.8924636840820312
2025-12-23 17:40:04.785 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:40:04.785 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:04.786 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2500，耗时: 1.009s
2025-12-23 17:40:04.786 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test111
2025-12-23 17:40:04.793 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:04.793 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:40:04.793 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2525
2025-12-23 17:40:04.859 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:04.889 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:40:04.889 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:05.119 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.230s
2025-12-23 17:40:05.119 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2301177978515625
2025-12-23 17:40:05.119 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:40:05.119 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:05.121 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2525，耗时: 0.328s
2025-12-23 17:40:05.121 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Info
2025-12-23 17:40:05.126 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:05.126 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:40:05.126 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2526
2025-12-23 17:40:05.195 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:05.225 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:40:05.225 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:05.579 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.355s
2025-12-23 17:40:05.579 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.3548133373260498
2025-12-23 17:40:05.580 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:40:05.581 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:05.581 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2526，耗时: 0.455s
2025-12-23 17:40:05.581 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Login User Routers
2025-12-23 17:40:05.589 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:05.589 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:40:05.589 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2527
2025-12-23 17:40:05.674 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:05.705 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:40:05.705 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:05.976 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.270s
2025-12-23 17:40:05.976 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2702009677886963
2025-12-23 17:40:05.976 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:40:05.977 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:05.977 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2527，耗时: 0.388s
2025-12-23 17:40:05.977 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get Api Script Library Script Library List
2025-12-23 17:40:06.007 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:06.007 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:40:06.008 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2528
2025-12-23 17:40:06.110 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:06.149 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:40:06.149 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:06.408 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.258s
2025-12-23 17:40:06.408 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.25905871391296387
2025-12-23 17:40:06.408 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:40:06.408 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:06.409 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2528，耗时: 0.401s
2025-12-23 17:40:06.409 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: Get System User List
2025-12-23 17:40:06.414 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:06.414 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:40:06.414 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2529
2025-12-23 17:40:06.510 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:06.549 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共0个
2025-12-23 17:40:06.550 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:07.449 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.899s
2025-12-23 17:40:07.451 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.9000754356384277
2025-12-23 17:40:07.452 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共0个
2025-12-23 17:40:07.452 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:07.453 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2529，耗时: 1.038s
2025-12-23 17:40:07.453 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: test_cases
2025-12-23 17:40:07.462 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:07.462 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:200 - 开始执行任务，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:40:07.462 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:54 - 开始执行API测试用例，ID: 2530
2025-12-23 17:40:07.529 |  | INFO     | module_admin.api_testing.api_cache_data.service.cache_data_service:get_cachedata_by_key:41 - 获取缓存；environment_cache:user:1:env:4:token
2025-12-23 17:40:07.593 |  | INFO     | utils.api_tools.executors.manager:execute_setup_list:25 - 开始执行前置脚本，共5个
2025-12-23 17:40:07.593 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - setup_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:07.871 |  | WARNING  | config.get_httpclient:on_request_end:39 - 整个请求耗时 0.278s
2025-12-23 17:40:07.873 |  | WARNING  | utils.api_tools.executors.api_request_exector:_send_request_with_info:236 - 接口发送获取响应阶段耗时0.2792627811431885
2025-12-23 17:40:07.874 |  | INFO     | utils.api_tools.executors.manager:execute_teardown_list:31 - 开始执行后置脚本，共6个
2025-12-23 17:40:07.874 |  | INFO     | utils.api_tools.executors.manager:_execute_list:91 - teardown_type 脚本执行完成，成功: 0, 失败: 0
2025-12-23 17:40:07.875 |  | INFO     | utils.api_workflow_tools.executors.api_case_executor:execute:72 - API测试用例执行完成，ID: 2530，耗时: 0.414s
2025-12-23 17:40:07.876 |  | INFO     | utils.api_workflow_tools.executors.factory:execute_task:206 - 任务执行完成，类型: TaskTypeEnum.APICASE，节点: 工作流模块树
2025-12-23 17:40:07.883 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [case_result] 成功
2025-12-23 17:40:07.887 |  | INFO     | utils.api_workflow_tools.workflow_visual_executor:execute_workflow_sync:202 - [log] 工作流执行完成
2025-12-23 17:40:07.936 |  | DEBUG    | config.get_websocket:_local_send_to_session:227 - [PID:22756] 本地发送成功: session_id=916639df-352b-4560-a189-7160bfffbf6f:notification
2025-12-23 17:40:07.937 |  | INFO     | config.get_websocket:_local_send_to_user:248 - [PID:22756] 本地发送给用户1成功: 1个会话
2025-12-23 17:40:07.936 |  | INFO     | config.get_websocket:send_to_user:305 - [PID:33344] 发送消息给用户1（已广播到所有Worker），本地发送: 0
2025-12-23 17:40:07.937 |  | INFO     | module_admin.websocket.service.websocket_service:send_to_user:35 - 通知用户: user_id=1, type=NotificationType.SUCCESS, sent=0
2025-12-23 17:40:07.944 |  | INFO     | module_task.scheduler_test:run_workflow_task:71 - [定时任务] 工作流 测试套件1 执行成功: 共8条, 成功8条, 耗时5.64秒
2025-12-23 17:40:07.944 |  | DEBUG    | config.get_scheduler:async_wrapper:378 - [Worker-f195f8f5] 任务函数执行完成: job_id=1
2025-12-23 17:40:08.123 | 965fa7e775194c6db914804e30c79007 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:32 - {'notification_id': None, 'user_id': None, 'notification_type': None, 'title': None, 'message': None, 'is_read': None, 'read_time': None, 'business_type': None, 'business_id': None, 'extra_data': None, 'create_by': None, 'create_time': None, 'update_by': None, 'update_time': None, 'remark': None, 'description': None, 'sort_no': None, 'del_flag': None, 'page_num': 1, 'page_size': 5}
2025-12-23 17:40:08.151 |  | DEBUG    | config.get_scheduler:release_lock:291 - [Worker-f195f8f5] 释放任务锁: job_id=1
2025-12-23 17:40:08.169 | 965fa7e775194c6db914804e30c79007 | INFO     | module_admin.system.notification.controller.notification_controller:get_task_notification_notification_list:41 - 获取成功
2025-12-23 17:40:08.172 |  | INFO     | middlewares.response_time_middleware:log_response_time:33 - GET /task_notification/notification/list - 200 - 226.65ms
INFO:     127.0.0.1:59252 - "GET /task_notification/notification/list?pageNum=1&pageSize=5 HTTP/1.1" 200 OK
2025-12-23 17:40:08.687 |  | DEBUG    | config.get_scheduler:try_acquire_lock:256 - [Worker-f195f8f5] 获取任务锁成功: job_id=1
2025-12-23 17:40:08.688 |  | INFO     | config.get_scheduler:async_wrapper:372 - [Worker-f195f8f5] 开始执行单例任务: job_id=1
2025-12-23 17