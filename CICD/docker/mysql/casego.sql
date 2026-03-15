/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 80012 (8.0.12)
 Source Host           : 127.0.0.1:3306
 Source Schema         : casego

 Target Server Type    : MySQL
 Target Server Version : 80012 (8.0.12)
 File Encoding         : 65001

 Date: 01/01/2026 08:55:50
*/
USE casego;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE `alembic_version`  (
  `version_num` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`version_num`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO `alembic_version` VALUES ('b9ac603e9e53');

-- ----------------------------
-- Table structure for api_assertions
-- ----------------------------
DROP TABLE IF EXISTS `api_assertions`;
CREATE TABLE `api_assertions`  (
  `assertion_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '断言ID',
  `case_id` int(11) NOT NULL COMMENT '关联的测试用例ID',
  `jsonpath` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'JSONPath表达式OR提取方法',
  `jsonpath_index` int(11) NULL DEFAULT NULL COMMENT 'JSONPath提取索引',
  `assertion_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '断言 (==, !=, >等)',
  `value` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '预期值',
  `assert_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '断言类型 (可选)',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否执行该断言',
  `extract_index_is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否执行提取索引操作',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`assertion_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2084 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口断言表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_assertions
-- ----------------------------

-- ----------------------------
-- Table structure for api_cache_data
-- ----------------------------
DROP TABLE IF EXISTS `api_cache_data`;
CREATE TABLE `api_cache_data`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '缓存数据ID',
  `cache_key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '缓存键名',
  `environment_id` int(11) NULL DEFAULT NULL COMMENT '关联的环境ID',
  `cache_value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '缓存值',
  `source_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据来源可以为空',
  `user_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用戶id',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 123216 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '环境缓存表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_cache_data
-- ----------------------------

-- ----------------------------
-- Table structure for api_cookies
-- ----------------------------
DROP TABLE IF EXISTS `api_cookies`;
CREATE TABLE `api_cookies`  (
  `cookie_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `case_id` int(11) NOT NULL COMMENT '关联的测试用例ID',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Cookie键名',
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'Cookie值',
  `domain` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '作用域',
  `path` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '路径',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用该Cookie',
  `is_required` tinyint(1) NULL DEFAULT NULL COMMENT '是否必填参数',
  `data_type` enum('STRING','INTEGER','BOOLEAN','NUMBER','ARRAY','FILE') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据类型',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`cookie_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2208 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口请求Cookie表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_cookies
-- ----------------------------

-- ----------------------------
-- Table structure for api_databases
-- ----------------------------
DROP TABLE IF EXISTS `api_databases`;
CREATE TABLE `api_databases`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '数据库ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据库名称',
  `db_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据库类型（如1 MySQL、2Redis，）',
  `host` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据库主机',
  `port` int(11) NOT NULL COMMENT '数据库端口',
  `username` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据库用户名',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '数据库密码',
  `project_id` int(11) NOT NULL COMMENT '所属项目ID',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '数据库配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_databases
-- ----------------------------
INSERT INTO `api_databases` VALUES (1, '测试环境mysql数据库', '1', '10.88.0.3', 3306, 'root', '123456', 1, 'admin', '2025-07-30 17:51:07', 'admin', '2026-01-01 08:53:09', NULL, NULL, NULL, 0);
INSERT INTO `api_databases` VALUES (2, '测试redis数据库', '2', '10.88.0.4', 6379, '', '123456', 1, 'admin', '2025-07-30 17:51:07', 'admin', '2026-01-01 08:53:16', NULL, NULL, NULL, 0);
INSERT INTO `api_databases` VALUES (3, '测试222项目数据库', '2', '111', 111, 'root', '123456', 2, 'admin', '2025-08-01 15:04:01', 'admin', '2025-08-01 17:59:26', NULL, NULL, NULL, 0);
INSERT INTO `api_databases` VALUES (4, '123123112', '2', '312312', 312312, '3123312', '21312', 13, 'admin', '2025-08-02 13:29:26', 'admin', '2025-08-02 13:29:26', NULL, NULL, NULL, 0);
INSERT INTO `api_databases` VALUES (5, '123123112', '2', '312312', 312312, '3123312', '21312', 13, 'admin', '2025-08-02 13:29:26', 'admin', '2025-08-02 13:29:26', NULL, NULL, NULL, 0);
INSERT INTO `api_databases` VALUES (6, '三号数据库', '1', '1111', 11111, '111', '1111', 1, 'admin', '2025-08-19 16:15:38', 'admin', '2025-08-19 16:15:38', NULL, NULL, 1, 0);
INSERT INTO `api_databases` VALUES (7, '1111111', '1', '2222222222', 333333333, '4444444', '4455555555', 42, 'guest', '2025-08-19 17:15:30', 'guest', '2025-08-19 17:15:30', NULL, NULL, 1, 0);
INSERT INTO `api_databases` VALUES (8, '111111113', '1', '127.0.0.1', 3306, 'ruoyi-fastapi', '123456', 47, 'admin', '2025-11-12 17:01:53', 'admin', '2025-11-12 17:07:46', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for api_environments
-- ----------------------------
DROP TABLE IF EXISTS `api_environments`;
CREATE TABLE `api_environments`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '环境ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '环境名称',
  `project_id` int(11) NULL DEFAULT NULL COMMENT '所属项目ID',
  `is_default` smallint(6) NULL DEFAULT NULL COMMENT '是否为默认环境',
  `request_timeout` int(11) NULL DEFAULT NULL COMMENT '请求超时(ms)',
  `global_headers` json NULL COMMENT '全局请求头json字典',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 171 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '环境配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_environments
-- ----------------------------
INSERT INTO `api_environments` VALUES (1, '正式环境', 1, 0, 5000, '[{\"key\": \"Authorization\", \"value\": \"Bearer {{token}}\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-07-30 23:31:33', 'admin', '2025-12-18 15:11:29', NULL, '', NULL, 0);
INSERT INTO `api_environments` VALUES (2, '测试环境', 1, 1, 6000, '[{\"key\": \"Authorization\", \"value\": \"Bearer {{token}}\", \"is_run\": true, \"description\": \"\"}, {\"key\": \"User-Agent\", \"value\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36\", \"is_run\": true, \"description\": \"\"}]', 'admin', '2025-07-30 23:31:47', 'admin', '2025-12-31 14:52:58', NULL, '123123', NULL, 0);
INSERT INTO `api_environments` VALUES (3, '灰度环境', 1, 0, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-07-30 23:36:27', 'admin', '2025-12-18 02:15:55', NULL, '', NULL, 0);
INSERT INTO `api_environments` VALUES (4, '演示环境', 1, 0, 5000, '[{\"key\": \"Authorization\", \"value\": \"Bearer {{token}}\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-07-30 23:36:35', 'admin', '2025-12-23 12:52:07', NULL, '', NULL, 0);
INSERT INTO `api_environments` VALUES (5, '测试环境', 2, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-07-31 17:49:14', 'admin', '2025-08-01 21:04:02', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (30, '正式環境', 13, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 22:58:25', 'admin', '2025-08-02 22:10:06', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (31, '測試環境', 13, 0, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 22:58:25', 'admin', '2025-08-01 22:58:25', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (32, '灰度環境', 13, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 22:58:25', 'admin', '2025-08-01 22:58:25', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (33, '演示環境', 13, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 22:58:25', 'admin', '2025-08-01 22:58:25', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (34, '正式環境', 14, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:47', 'admin', '2025-08-01 23:01:47', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (35, '測試環境', 14, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:47', 'admin', '2025-08-01 23:01:47', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (36, '灰度環境', 14, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:47', 'admin', '2025-08-01 23:01:47', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (37, '演示環境', 14, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:47', 'admin', '2025-08-01 23:01:47', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (38, '正式環境', 15, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:53', 'admin', '2025-08-01 23:01:53', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (39, '測試環境', 15, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:53', 'admin', '2025-08-01 23:01:53', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (40, '灰度環境', 15, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:53', 'admin', '2025-08-01 23:01:53', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (41, '演示環境', 15, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:01:53', 'admin', '2025-08-01 23:01:53', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (42, '正式環境', 16, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:10:34', 'admin', '2025-08-01 23:10:34', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (43, '測試環境', 16, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:10:34', 'admin', '2025-08-01 23:10:34', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (44, '灰度環境', 16, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:10:34', 'admin', '2025-08-01 23:10:34', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (45, '演示環境', 16, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-01 23:10:34', 'admin', '2025-08-01 23:10:34', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (46, '天选之人', 13, 0, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-02 09:08:35', 'guest', '2025-08-02 09:08:35', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (47, '正式環境', 17, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-02 09:54:16', 'guest', '2025-08-02 09:54:16', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (48, '測試環境', 17, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-02 09:54:16', 'guest', '2025-08-02 09:54:16', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (49, '灰度環境', 17, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-02 09:54:16', 'guest', '2025-08-02 09:54:16', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (50, '演示環境', 17, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-02 09:54:16', 'guest', '2025-08-02 09:54:16', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (51, '123', 1, 0, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 21:45:56', 'admin', '2025-08-07 21:45:56', '123', NULL, NULL, 1);
INSERT INTO `api_environments` VALUES (52, '9999', 1, 0, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 21:46:08', 'admin', '2025-08-07 21:46:08', NULL, NULL, NULL, 1);
INSERT INTO `api_environments` VALUES (53, '正式環境', 18, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 21:47:12', 'admin', '2025-08-07 21:47:12', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (54, '測試環境', 18, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 21:47:12', 'admin', '2025-08-07 21:47:12', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (55, '灰度環境', 18, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 21:47:12', 'admin', '2025-08-07 21:47:12', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (56, '演示環境', 18, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 21:47:12', 'admin', '2025-08-07 21:47:12', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (129, '正式環境', 38, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (130, '測試環境', 38, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (131, '灰度環境', 38, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (132, '演示環境', 38, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (133, '正式環境', 39, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (134, '測試環境', 39, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (135, '灰度環境', 39, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (136, '演示環境', 39, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (137, '正式環境', 40, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (138, '測試環境', 40, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (139, '灰度環境', 40, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (140, '演示環境', 40, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (141, '正式環境', 41, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (142, '測試環境', 41, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (143, '灰度環境', 41, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (144, '演示環境', 41, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (145, '正式環境', 42, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:14:46', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (146, '測試環境', 42, 1, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:14:50', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (147, '灰度環境', 42, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:14:48', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (148, '演示環境', 42, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:13:29', NULL, NULL, NULL, 0);
INSERT INTO `api_environments` VALUES (149, '213', 1, NULL, 5000, '[{\"key\": \"1\", \"value\": \"22\", \"is_run\": true, \"description\": \"是的\"}]', 'admin', '2025-08-19 17:31:29', 'admin', '2025-08-19 13:19:38', NULL, NULL, 1, 1);
INSERT INTO `api_environments` VALUES (150, '正式環境', 43, NULL, 5000, '[]', 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (151, '測試環境', 43, 1, 5000, '[]', 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (152, '灰度環境', 43, NULL, 5000, '[]', 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (153, '演示環境', 43, NULL, 5000, '[]', 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (154, '正式環境', 44, NULL, 5000, '[]', 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (155, '測試環境', 44, 1, 5000, '[]', 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (156, '灰度環境', 44, NULL, 5000, '[]', 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (157, '演示環境', 44, NULL, 5000, '[]', 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (158, '正式環境', 45, NULL, 5000, '[]', 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (159, '測試環境', 45, 1, 5000, '[]', 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (160, '灰度環境', 45, NULL, 5000, '[]', 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (161, '演示環境', 45, NULL, 5000, '[]', 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (162, '正式環境', 46, NULL, 5000, '[]', 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (163, '測試環境', 46, 1, 5000, '[]', 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (164, '灰度環境', 46, NULL, 5000, '[]', 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (165, '演示環境', 46, NULL, 5000, '[]', 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (166, '123123', 1, NULL, 5000, '[]', 'admin', '2025-09-12 09:53:08', 'admin', '2025-09-12 03:27:04', '123123', NULL, 1, 1);
INSERT INTO `api_environments` VALUES (167, '正式環境', 47, NULL, 5000, '[]', 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (168, '測試環境', 47, 1, 5000, '[]', 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (169, '灰度環境', 47, NULL, 5000, '[]', 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);
INSERT INTO `api_environments` VALUES (170, '演示環境', 47, NULL, 5000, '[]', 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for api_formdata
-- ----------------------------
DROP TABLE IF EXISTS `api_formdata`;
CREATE TABLE `api_formdata`  (
  `formdata_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `case_id` int(11) NOT NULL COMMENT '关联的测试用例ID',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '键名',
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '表单值',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用该表单值',
  `is_required` tinyint(1) NULL DEFAULT NULL COMMENT '是否必填',
  `data_type` enum('STRING','INTEGER','BOOLEAN','NUMBER','ARRAY','FILE') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据类型',
  `form_file_config` json NULL COMMENT 'formdata的文件配置',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`formdata_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 6412 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口表单body' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_formdata
-- ----------------------------
INSERT INTO `api_formdata` VALUES (6410, 3668, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6411, 3668, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6409, 3668, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6408, 3668, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6407, 3668, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6406, 3668, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6405, 3668, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6404, 3668, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6403, 3668, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6402, 3668, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6401, 3668, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6400, 3668, 'scriptContent', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6399, 3668, 'scriptType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6398, 3668, 'scriptName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6397, 3668, 'scriptId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6396, 3662, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6395, 3662, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6394, 3662, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6393, 3662, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6392, 3662, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6391, 3662, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6390, 3662, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6389, 3662, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6388, 3662, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6387, 3662, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6386, 3662, 'extraData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6385, 3662, 'businessId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6384, 3662, 'businessType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6383, 3662, 'readTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6382, 3662, 'isRead', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6381, 3662, 'message', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6380, 3662, 'title', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6379, 3662, 'notificationType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6378, 3662, 'userId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6377, 3662, 'notificationId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6376, 3654, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6375, 3654, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6374, 3654, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6373, 3654, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6372, 3654, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6371, 3654, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6370, 3654, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6369, 3654, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6368, 3654, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6367, 3654, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6366, 3654, 'triggerType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6365, 3654, 'reportData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6364, 3654, 'isSuccess', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6363, 3654, 'duration', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6362, 3654, 'failedCases', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6361, 3654, 'successCases', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6360, 3654, 'totalCases', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6359, 3654, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6358, 3654, 'startTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6357, 3654, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6356, 3654, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6355, 3654, 'reportId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6354, 3648, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6353, 3648, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6352, 3648, 'item', '{}', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6351, 3648, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6350, 3648, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6349, 3648, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6348, 3648, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6347, 3648, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6346, 3648, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6345, 3648, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6344, 3648, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6343, 3648, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6342, 3648, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6341, 3648, 'groupName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6340, 3648, 'parameterizationId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6339, 3648, 'keyId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6338, 3642, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6337, 3642, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6336, 3642, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6335, 3642, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6334, 3642, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6333, 3642, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6332, 3642, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6331, 3642, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6330, 3642, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6329, 3642, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6328, 3642, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6327, 3642, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6326, 3642, 'parameterizationId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6325, 3633, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6324, 3633, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6323, 3633, 'eventType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6322, 3633, 'reportId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6321, 3633, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6320, 3633, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6319, 3633, 'path', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6318, 3633, 'method', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6317, 3633, 'delFlag', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6316, 3633, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6315, 3633, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6314, 3633, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6313, 3633, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6312, 3633, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6311, 3633, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6310, 3633, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6309, 3633, 'assertionSuccess', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6308, 3633, 'responseTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6307, 3633, 'responseStatusCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6306, 3633, 'executionData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6305, 3633, 'isSuccess', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6304, 3633, 'executionTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6303, 3633, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6302, 3633, 'logId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6301, 3627, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6300, 3627, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6299, 3627, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6298, 3627, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6297, 3627, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6296, 3627, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6295, 3627, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6294, 3627, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6293, 3627, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6292, 3627, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6291, 3627, 'config', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6290, 3627, 'childrenIds', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6289, 3627, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6288, 3627, 'type', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6287, 3627, 'name', '未命名', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6286, 3627, 'parentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6285, 3627, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6284, 3627, 'nodeId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6283, 3619, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6282, 3619, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6281, 3619, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6280, 3619, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6279, 3619, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6270, 3619, 'errorMessage', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6269, 3619, 'conditionResult', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6268, 3619, 'loopItem', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6267, 3619, 'loopIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6266, 3619, 'contextSnapshot', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6265, 3619, 'outputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6264, 3619, 'inputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6263, 3619, 'duration', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6262, 3619, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6261, 3619, 'startTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6260, 3619, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6259, 3619, 'nodeId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6258, 3619, 'workflowExecutionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6257, 3619, 'nodeExecutionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6256, 3613, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6255, 3613, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6254, 3613, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6253, 3613, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6252, 3613, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6251, 3613, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6250, 3613, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6249, 3613, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6248, 3613, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6247, 3613, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6246, 3613, 'errorDetails', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6245, 3613, 'errorMessage', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6244, 3613, 'skippedNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6243, 3613, 'failedNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6242, 3613, 'successNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6241, 3613, 'totalNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6240, 3613, 'contextData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6239, 3613, 'outputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6238, 3613, 'inputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6237, 3613, 'duration', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6236, 3613, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6235, 3613, 'startTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6234, 3613, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6233, 3613, 'workflowName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6232, 3613, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6231, 3613, 'workflowExecutionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6230, 3606, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6229, 3606, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6228, 3606, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6227, 3606, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6226, 3606, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6225, 3606, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6224, 3606, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6223, 3606, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6222, 3606, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6221, 3606, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6220, 3606, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6219, 3606, 'parentSubmoduleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6218, 3606, 'executionConfig', '{\'parameterizationData\': [], \'loopCount\': 1, \'threadingCount\': 1}', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6217, 3606, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6216, 3606, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6215, 3598, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6214, 3598, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6213, 3598, 'formFileConfig', '[]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6212, 3598, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6211, 3598, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6210, 3598, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6209, 3598, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6208, 3598, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6207, 3598, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6206, 3598, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6205, 3598, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6204, 3598, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6203, 3598, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6202, 3598, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6201, 3598, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6200, 3598, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6199, 3598, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6198, 3598, 'formdataId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6197, 3592, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6196, 3592, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6195, 3592, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6194, 3592, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6193, 3592, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6192, 3592, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6191, 3592, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6190, 3592, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6189, 3592, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6188, 3592, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6187, 3592, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6186, 3592, 'waitTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6185, 3592, 'script', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6184, 3592, 'dbOperation', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6183, 3592, 'databaseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6182, 3592, 'responseCookie', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6181, 3592, 'responseHeader', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6180, 3592, 'xpathExpression', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6179, 3592, 'regularExpression', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6178, 3592, 'extractVariables', '[{}]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6177, 3592, 'variableName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6176, 3592, 'extractIndexIsRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6175, 3592, 'extractIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6174, 3592, 'jsonpath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6173, 3592, 'extractVariableMethod', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6172, 3592, 'teardownType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6171, 3592, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6170, 3592, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6169, 3592, 'teardownId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6168, 3586, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6167, 3586, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6166, 3586, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6165, 3586, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6164, 3586, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6163, 3586, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6162, 3586, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6161, 3586, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6160, 3586, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6159, 3586, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6158, 3586, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6157, 3586, 'extractIndexIsRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6156, 3586, 'extractIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6155, 3586, 'waitTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6154, 3586, 'variableName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6153, 3586, 'jsonpath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6152, 3586, 'extractVariables', '[{}]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6151, 3586, 'script', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6150, 3586, 'dbConnectionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6149, 3586, 'setupType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6148, 3586, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6147, 3586, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6146, 3586, 'setupId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6145, 3580, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6144, 3580, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6143, 3580, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6142, 3580, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6141, 3580, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6140, 3580, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6139, 3580, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6138, 3580, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6137, 3580, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6136, 3580, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6135, 3580, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6134, 3580, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6133, 3580, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6132, 3580, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6131, 3580, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6130, 3580, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6129, 3580, 'paramId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6128, 3574, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6127, 3574, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6126, 3574, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6125, 3574, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6124, 3574, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6123, 3574, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6122, 3574, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6121, 3574, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6120, 3574, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6119, 3574, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6118, 3574, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6117, 3574, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6116, 3574, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6115, 3574, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6114, 3574, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6113, 3574, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6112, 3574, 'headerId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6111, 3568, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6110, 3568, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6109, 3568, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6108, 3568, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6107, 3568, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6106, 3568, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6105, 3568, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6104, 3568, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6103, 3568, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6102, 3568, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6101, 3568, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6100, 3568, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6099, 3568, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6098, 3568, 'path', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6097, 3568, 'domain', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6096, 3568, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6095, 3568, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6094, 3568, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6093, 3568, 'cookieId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6092, 3562, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6091, 3562, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6090, 3562, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6089, 3562, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6088, 3562, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6086, 3562, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6087, 3562, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6085, 3562, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6084, 3562, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6083, 3562, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6082, 3562, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6081, 3562, 'assertType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6080, 3562, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6079, 3562, 'assertionMethod', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6078, 3562, 'extractIndexIsRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6077, 3562, 'jsonpathIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6076, 3562, 'jsonpath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6075, 3562, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6074, 3562, 'assertionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6073, 3555, 'selectedApis', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6072, 3555, 'urlKeywords', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6071, 3555, 'includeDomains', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6070, 3555, 'allowedMethods', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6069, 3555, 'filterStatic', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6068, 3555, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6067, 3555, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6066, 3555, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6065, 3555, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6064, 3555, 'moduleName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6063, 3555, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6062, 3555, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6061, 3555, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6060, 3554, 'urlKeywords', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6059, 3554, 'includeDomains', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6058, 3554, 'allowedMethods', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6057, 3554, 'filterStatic', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6056, 3554, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6055, 3554, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6054, 3554, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6053, 3554, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6052, 3554, 'moduleName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6051, 3554, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6050, 3554, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6049, 3554, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6048, 3553, 'selectedApis', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6047, 3553, 'selectedModules', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6046, 3553, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6045, 3553, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6044, 3553, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6043, 3553, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6042, 3553, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6041, 3553, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6040, 3553, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6039, 3553, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6038, 3553, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6037, 3553, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6036, 3552, 'selectedApis', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6035, 3552, 'selectedModules', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6034, 3552, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6033, 3552, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6032, 3552, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6031, 3552, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6030, 3552, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6029, 3552, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6028, 3552, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6027, 3552, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6026, 3552, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6025, 3552, 'url', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6024, 3551, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6023, 3551, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6022, 3551, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6021, 3551, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6020, 3551, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6019, 3551, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6018, 3550, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6017, 3550, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6016, 3550, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6015, 3550, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6014, 3550, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6013, 3550, 'url', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6012, 3549, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6011, 3549, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6010, 3549, 'responseExample', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6009, 3549, 'caseFileConfig', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6008, 3549, 'jsonData', '{}', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6007, 3549, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6006, 3549, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6005, 3549, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6004, 3549, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6003, 3549, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6002, 3549, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6001, 3549, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6000, 3549, 'sleep', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5999, 3549, 'statusCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5998, 3549, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5997, 3549, 'requestType', 'NONE', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5996, 3549, 'method', 'GET', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5995, 3549, 'path', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5994, 3549, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5993, 3549, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5992, 3549, 'parentSubmoduleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5991, 3549, 'parentCaseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5990, 3549, 'copyId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5989, 3549, 'caseType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5988, 3549, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5987, 3549, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5986, 3539, 'uploadTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5985, 3539, 'fileType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5984, 3539, 'fileSize', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5983, 3539, 'fileName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5982, 3539, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5981, 3539, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5980, 3539, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5979, 3538, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5978, 3538, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5977, 3538, 'userId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5976, 3538, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5975, 3538, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5974, 3538, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5973, 3538, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5972, 3538, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5971, 3538, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5970, 3538, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5969, 3538, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5968, 3538, 'sourceType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5967, 3538, 'cacheValue', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5966, 3538, 'environmentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5965, 3538, 'cacheKey', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5964, 3538, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5963, 3532, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5962, 3532, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5961, 3532, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5960, 3532, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5959, 3532, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5958, 3532, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5957, 3532, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5956, 3532, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5955, 3532, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5954, 3532, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5953, 3532, 'isDefault', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5952, 3532, 'environmentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5951, 3532, 'url', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5950, 3532, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5949, 3532, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5948, 3526, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5947, 3526, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5946, 3526, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5945, 3526, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5944, 3526, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5943, 3526, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5942, 3526, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5941, 3526, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5940, 3526, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5939, 3526, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5938, 3526, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5937, 3526, 'ancestors', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5936, 3526, 'parentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5935, 3526, 'type', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5934, 3526, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5933, 3526, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5932, 3516, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5931, 3516, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5930, 3516, 'globalHeaders', '[{\'description\': \'内容类型\', \'is_run\': True, \'key\': \'Content-Type\', \'value\': \'application/json\'}]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5929, 3516, 'requestTimeout', '5000', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5928, 3516, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5927, 3516, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5926, 3516, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5925, 3516, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5924, 3516, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5923, 3516, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5922, 3516, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5921, 3516, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5920, 3516, 'isDefault', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5919, 3516, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5918, 3516, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5917, 3516, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5916, 3506, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5915, 3506, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5914, 3506, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5913, 3506, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5912, 3506, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5911, 3506, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5910, 3506, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5909, 3506, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5908, 3506, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5907, 3506, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5906, 3506, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5905, 3506, 'password', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5904, 3506, 'username', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5903, 3506, 'port', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5902, 3506, 'host', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5901, 3506, 'dbType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5900, 3506, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5899, 3506, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5898, 3500, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5897, 3500, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5896, 3500, 'ancestors', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5895, 3500, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5894, 3500, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5893, 3500, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5892, 3500, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5891, 3500, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5890, 3500, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5889, 3500, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5888, 3500, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5887, 3500, 'parentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5886, 3500, 'type', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5885, 3500, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5884, 3500, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5883, 3481, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5882, 3472, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5881, 3472, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5880, 3472, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5879, 3472, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5878, 3472, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5877, 3472, 'exceptionInfo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5876, 3472, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5875, 3472, 'jobMessage', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5874, 3472, 'jobTrigger', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5873, 3472, 'jobKwargs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5872, 3472, 'jobArgs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5871, 3472, 'invokeTarget', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5870, 3472, 'jobExecutor', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5869, 3472, 'jobGroup', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5868, 3472, 'jobName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5867, 3472, 'jobLogId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5866, 3468, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5865, 3468, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5864, 3468, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5863, 3468, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5862, 3468, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5861, 3468, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5860, 3468, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5859, 3468, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5858, 3468, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5857, 3468, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5856, 3468, 'concurrent', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5855, 3468, 'misfirePolicy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5854, 3468, 'cronExpression', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5853, 3468, 'jobKwargs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5852, 3468, 'jobArgs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5851, 3468, 'invokeTarget', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5850, 3468, 'jobExecutor', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5849, 3468, 'jobGroup', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5848, 3468, 'jobName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5847, 3468, 'jobId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5846, 3458, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5845, 3458, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5844, 3458, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5843, 3458, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5842, 3458, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5841, 3458, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5840, 3458, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5839, 3458, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5838, 3458, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5837, 3458, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5836, 3458, 'bizTag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5835, 3458, 'fileHash', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5834, 3458, 'isTemp', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5833, 3458, 'storageType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5832, 3458, 'fileUrl', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5831, 3458, 'filePath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5830, 3458, 'fileSize', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5829, 3458, 'mimeType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5828, 3458, 'fileExt', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5827, 3458, 'storedName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5826, 3458, 'originalName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5825, 3458, 'fileId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5824, 3451, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5823, 3450, 'files', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5822, 3449, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5821, 3449, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5820, 3449, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5819, 3449, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5818, 3449, 'isAsc', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5817, 3449, 'orderByColumn', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5816, 3449, 'loginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5815, 3449, 'msg', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5814, 3449, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5813, 3449, 'os', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5812, 3449, 'browser', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5811, 3449, 'loginLocation', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5810, 3449, 'ipaddr', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5809, 3449, 'userName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5808, 3449, 'infoId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5807, 3444, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5806, 3444, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5805, 3444, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5804, 3444, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5803, 3444, 'isAsc', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5802, 3444, 'orderByColumn', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5801, 3444, 'costTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5800, 3444, 'operTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5799, 3444, 'errorMsg', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5798, 3444, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5797, 3444, 'jsonResult', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5796, 3444, 'operParam', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5795, 3444, 'operLocation', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5794, 3444, 'operIp', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5793, 3444, 'operUrl', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5792, 3444, 'deptName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5791, 3444, 'operName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5790, 3444, 'operatorType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5789, 3444, 'requestMethod', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5788, 3444, 'method', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5787, 3444, 'businessType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5786, 3444, 'title', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5785, 3444, 'operId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5784, 3435, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5783, 3435, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5782, 3435, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5781, 3435, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5780, 3435, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5779, 3435, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5778, 3435, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5777, 3435, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5776, 3435, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5775, 3435, 'configType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5774, 3435, 'configValue', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5773, 3435, 'configKey', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5772, 3435, 'configName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5771, 3435, 'configId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5770, 3427, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5769, 3427, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5768, 3427, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5767, 3427, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5766, 3427, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5765, 3427, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5764, 3427, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5763, 3427, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5762, 3427, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5761, 3427, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5760, 3427, 'isDefault', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5759, 3427, 'listClass', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5758, 3427, 'cssClass', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5757, 3427, 'dictType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5756, 3427, 'dictValue', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5755, 3427, 'dictLabel', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5754, 3427, 'dictSort', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5753, 3427, 'dictCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5752, 3420, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5751, 3420, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5750, 3420, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5749, 3420, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5748, 3420, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5747, 3420, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5746, 3420, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5745, 3420, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5744, 3420, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5743, 3420, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5742, 3420, 'dictType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5741, 3420, 'dictName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5740, 3420, 'dictId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5739, 3412, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5738, 3412, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5737, 3412, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5736, 3412, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5735, 3412, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5734, 3412, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5733, 3412, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5732, 3412, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5731, 3412, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5730, 3412, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5729, 3412, 'postSort', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5728, 3412, 'postName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5727, 3412, 'postCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5726, 3412, 'postId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5725, 3387, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6278, 3619, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6276, 3619, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6275, 3619, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6274, 3619, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6273, 3619, 'createdAt', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6272, 3619, 'retryCount', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6271, 3619, 'errorDetails', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (6277, 3619, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5724, 3387, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5723, 3387, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5722, 3387, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5721, 3387, 'admin', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5720, 3387, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5719, 3387, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5718, 3387, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5717, 3387, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5716, 3387, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5715, 3387, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5714, 3387, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5713, 3387, 'deptCheckStrictly', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5712, 3387, 'menuCheckStrictly', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5711, 3387, 'dataScope', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5710, 3387, 'roleSort', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5709, 3387, 'roleKey', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5708, 3387, 'roleName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5707, 3387, 'roleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5706, 3377, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5705, 3377, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5704, 3377, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5703, 3377, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5702, 3377, 'admin', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5701, 3377, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5700, 3377, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5699, 3377, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5698, 3377, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5697, 3377, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5696, 3377, 'loginDate', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5695, 3377, 'loginIp', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5694, 3377, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5693, 3377, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5692, 3377, 'password', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5691, 3377, 'avatar', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5690, 3377, 'sex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5689, 3377, 'phonenumber', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5688, 3377, 'email', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5687, 3377, 'userType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5686, 3377, 'nickName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5685, 3377, 'userName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5684, 3377, 'deptId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5683, 3377, 'userId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5682, 3375, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5681, 3373, 'avatarfile', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5680, 3356, 'login_info', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5679, 3356, 'uuid', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5678, 3356, 'code', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5677, 3356, 'client_secret', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5676, 3356, 'client_id', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5675, 3356, 'scope', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5674, 3356, 'password', 'admin123', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5673, 3356, 'username', 'admin', 1, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5672, 3356, 'grant_type', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:29', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (5671, 3349, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5670, 3349, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5669, 3349, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5668, 3349, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5667, 3349, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5666, 3349, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5665, 3349, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5664, 3349, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5663, 3349, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5662, 3349, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5661, 3349, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5660, 3349, 'scriptContent', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5659, 3349, 'scriptType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5658, 3349, 'scriptName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5657, 3349, 'scriptId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5656, 3343, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5655, 3343, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5654, 3343, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5653, 3343, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5652, 3343, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5651, 3343, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5650, 3343, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5649, 3343, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5648, 3343, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5647, 3343, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5646, 3343, 'extraData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5645, 3343, 'businessId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5644, 3343, 'businessType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5643, 3343, 'readTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5642, 3343, 'isRead', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5641, 3343, 'message', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5640, 3343, 'title', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5638, 3343, 'userId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5639, 3343, 'notificationType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5637, 3343, 'notificationId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5636, 3335, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5635, 3335, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5634, 3335, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5633, 3335, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5632, 3335, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5631, 3335, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5630, 3335, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5629, 3335, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5628, 3335, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5627, 3335, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5626, 3335, 'triggerType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5625, 3335, 'reportData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5624, 3335, 'isSuccess', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5623, 3335, 'duration', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5622, 3335, 'failedCases', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5621, 3335, 'successCases', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5620, 3335, 'totalCases', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5619, 3335, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5618, 3335, 'startTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5617, 3335, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5616, 3335, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5615, 3335, 'reportId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5614, 3329, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5613, 3329, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5612, 3329, 'item', '{}', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5611, 3329, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5610, 3329, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5609, 3329, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5608, 3329, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5607, 3329, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5606, 3329, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5605, 3329, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5604, 3329, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5603, 3329, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5602, 3329, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5601, 3329, 'groupName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5600, 3329, 'parameterizationId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5599, 3329, 'keyId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5598, 3323, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5597, 3323, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5596, 3323, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5595, 3323, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5594, 3323, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5593, 3323, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5592, 3323, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5591, 3323, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5590, 3323, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5589, 3323, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5588, 3323, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5587, 3323, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5586, 3323, 'parameterizationId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5585, 3314, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5584, 3314, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5583, 3314, 'eventType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5582, 3314, 'reportId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5580, 3314, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5579, 3314, 'path', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5578, 3314, 'method', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5577, 3314, 'delFlag', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5576, 3314, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5575, 3314, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5581, 3314, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5574, 3314, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5573, 3314, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5572, 3314, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5571, 3314, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5570, 3314, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5569, 3314, 'assertionSuccess', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5568, 3314, 'responseTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5567, 3314, 'responseStatusCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5566, 3314, 'executionData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5565, 3314, 'isSuccess', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5564, 3314, 'executionTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5563, 3314, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5562, 3314, 'logId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5561, 3308, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5560, 3308, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5559, 3308, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5558, 3308, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5557, 3308, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5556, 3308, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5555, 3308, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5554, 3308, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5553, 3308, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5552, 3308, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5551, 3308, 'config', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5550, 3308, 'childrenIds', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5549, 3308, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5548, 3308, 'type', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5547, 3308, 'name', '未命名', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5546, 3308, 'parentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5545, 3308, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5544, 3308, 'nodeId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5543, 3300, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5542, 3300, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5541, 3300, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5538, 3300, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5539, 3300, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5540, 3300, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5537, 3300, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5536, 3300, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5535, 3300, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5534, 3300, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5533, 3300, 'createdAt', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5532, 3300, 'retryCount', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5531, 3300, 'errorDetails', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5528, 3300, 'loopItem', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5529, 3300, 'conditionResult', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5530, 3300, 'errorMessage', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5527, 3300, 'loopIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5526, 3300, 'contextSnapshot', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5525, 3300, 'outputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5524, 3300, 'inputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5523, 3300, 'duration', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5522, 3300, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5521, 3300, 'startTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5520, 3300, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5519, 3300, 'nodeId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5518, 3300, 'workflowExecutionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5517, 3300, 'nodeExecutionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5516, 3294, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5515, 3294, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5514, 3294, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5513, 3294, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5512, 3294, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5511, 3294, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5510, 3294, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5509, 3294, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5508, 3294, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5507, 3294, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5506, 3294, 'errorDetails', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5505, 3294, 'errorMessage', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5504, 3294, 'skippedNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5503, 3294, 'failedNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5502, 3294, 'successNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5501, 3294, 'totalNodes', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5500, 3294, 'contextData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5499, 3294, 'outputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5498, 3294, 'inputData', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5497, 3294, 'duration', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5496, 3294, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5495, 3294, 'startTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5494, 3294, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5493, 3294, 'workflowName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5492, 3294, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5491, 3294, 'workflowExecutionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5490, 3287, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5489, 3287, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5488, 3287, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5487, 3287, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5486, 3287, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5485, 3287, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5484, 3287, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5483, 3287, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5482, 3287, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5481, 3287, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5480, 3287, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5479, 3287, 'parentSubmoduleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5478, 3287, 'executionConfig', '{\'parameterizationData\': [], \'loopCount\': 1, \'threadingCount\': 1}', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5477, 3287, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5476, 3287, 'workflowId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5475, 3279, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5474, 3279, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5473, 3279, 'formFileConfig', '[]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5472, 3279, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5471, 3279, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5470, 3279, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5469, 3279, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5468, 3279, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5467, 3279, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5466, 3279, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5465, 3279, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5464, 3279, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5463, 3279, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5462, 3279, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5461, 3279, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5460, 3279, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5459, 3279, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5458, 3279, 'formdataId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5457, 3273, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5456, 3273, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5455, 3273, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5454, 3273, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5453, 3273, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5452, 3273, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5451, 3273, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5450, 3273, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5449, 3273, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5448, 3273, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5447, 3273, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5446, 3273, 'waitTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5445, 3273, 'script', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5444, 3273, 'dbOperation', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5443, 3273, 'databaseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5442, 3273, 'responseCookie', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5441, 3273, 'responseHeader', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5440, 3273, 'xpathExpression', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5439, 3273, 'regularExpression', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5438, 3273, 'extractVariables', '[{}]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5437, 3273, 'variableName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5436, 3273, 'extractIndexIsRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5435, 3273, 'extractIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5434, 3273, 'jsonpath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5433, 3273, 'extractVariableMethod', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5432, 3273, 'teardownType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5431, 3273, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5430, 3273, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5429, 3273, 'teardownId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5428, 3267, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5427, 3267, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5426, 3267, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5425, 3267, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5424, 3267, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5423, 3267, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5422, 3267, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5421, 3267, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5420, 3267, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5419, 3267, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5418, 3267, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5417, 3267, 'extractIndexIsRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5416, 3267, 'extractIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5415, 3267, 'waitTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5414, 3267, 'variableName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5413, 3267, 'jsonpath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5412, 3267, 'extractVariables', '[{}]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5411, 3267, 'script', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5410, 3267, 'dbConnectionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5409, 3267, 'setupType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5408, 3267, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5407, 3267, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5406, 3267, 'setupId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5405, 3261, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5404, 3261, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5403, 3261, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5402, 3261, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5401, 3261, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5400, 3261, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5399, 3261, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5398, 3261, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5397, 3261, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5396, 3261, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5395, 3261, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5394, 3261, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5393, 3261, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5392, 3261, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5391, 3261, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5390, 3261, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5389, 3261, 'paramId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5388, 3255, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5387, 3255, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5386, 3255, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5385, 3255, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5384, 3255, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5383, 3255, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5382, 3255, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5381, 3255, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5380, 3255, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5379, 3255, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5378, 3255, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5377, 3255, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5376, 3255, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5375, 3255, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5374, 3255, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5373, 3255, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5372, 3255, 'headerId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5371, 3249, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5370, 3249, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5369, 3249, 'dataType', 'string', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5368, 3249, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5367, 3249, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5366, 3249, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5365, 3249, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5364, 3249, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5363, 3249, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5362, 3249, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5361, 3249, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5360, 3249, 'isRequired', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5359, 3249, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5358, 3249, 'path', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5357, 3249, 'domain', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5356, 3249, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5355, 3249, 'key', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5354, 3249, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5353, 3249, 'cookieId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5352, 3243, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5351, 3243, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5350, 3243, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5349, 3243, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5348, 3243, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5347, 3243, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5346, 3243, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5345, 3243, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5344, 3243, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5342, 3243, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5343, 3243, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5341, 3243, 'assertType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5340, 3243, 'value', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5338, 3243, 'extractIndexIsRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5337, 3243, 'jsonpathIndex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5336, 3243, 'jsonpath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5335, 3243, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5334, 3243, 'assertionId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5333, 3236, 'selectedApis', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5339, 3243, 'assertionMethod', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5332, 3236, 'urlKeywords', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5331, 3236, 'includeDomains', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5329, 3236, 'filterStatic', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5328, 3236, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5327, 3236, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5326, 3236, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5324, 3236, 'moduleName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5330, 3236, 'allowedMethods', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5325, 3236, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5323, 3236, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5322, 3236, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5321, 3236, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5320, 3235, 'urlKeywords', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5319, 3235, 'includeDomains', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5318, 3235, 'allowedMethods', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5317, 3235, 'filterStatic', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5316, 3235, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5315, 3235, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5314, 3235, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5313, 3235, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5312, 3235, 'moduleName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5311, 3235, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5310, 3235, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5309, 3235, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5308, 3234, 'selectedApis', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5307, 3234, 'selectedModules', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5306, 3234, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5305, 3234, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5304, 3234, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5303, 3234, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5302, 3234, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5301, 3234, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5300, 3234, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5299, 3234, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5298, 3234, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5297, 3234, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5296, 3233, 'selectedApis', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5295, 3233, 'selectedModules', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5294, 3233, 'importCookies', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5293, 3233, 'importBody', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5292, 3233, 'importParams', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5291, 3233, 'importHeaders', 'True', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5290, 3233, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5289, 3233, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5288, 3233, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5287, 3233, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5286, 3233, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5285, 3233, 'url', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5284, 3232, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5283, 3232, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5282, 3232, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5281, 3232, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5280, 3232, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5279, 3232, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5278, 3231, 'includeDeprecated', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5277, 3231, 'conflictStrategy', 'smart_merge', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5276, 3231, 'moduleStrategy', 'auto_match', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5275, 3231, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5274, 3231, 'projectId', '0', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5273, 3231, 'url', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5272, 3230, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5271, 3230, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5270, 3230, 'responseExample', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5268, 3230, 'jsonData', '{}', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5269, 3230, 'caseFileConfig', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5267, 3230, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5266, 3230, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5265, 3230, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5264, 3230, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5263, 3230, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5262, 3230, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5261, 3230, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5260, 3230, 'sleep', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5259, 3230, 'statusCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5258, 3230, 'isRun', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5257, 3230, 'requestType', 'NONE', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5256, 3230, 'method', 'GET', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5255, 3230, 'path', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5254, 3230, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5253, 3230, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5252, 3230, 'parentSubmoduleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5251, 3230, 'parentCaseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5250, 3230, 'copyId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5249, 3230, 'caseType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5248, 3230, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5247, 3230, 'caseId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5246, 3220, 'uploadTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5245, 3220, 'fileType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5244, 3220, 'fileSize', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5243, 3220, 'fileName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5242, 3220, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5241, 3220, 'targetModuleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5240, 3220, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5239, 3219, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5238, 3219, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5237, 3219, 'userId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5236, 3219, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5235, 3219, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5234, 3219, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5233, 3219, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5232, 3219, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5231, 3219, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5230, 3219, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5229, 3219, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5228, 3219, 'sourceType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5227, 3219, 'cacheValue', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5226, 3219, 'environmentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5225, 3219, 'cacheKey', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5224, 3219, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5223, 3213, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5222, 3213, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5221, 3213, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5220, 3213, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5219, 3213, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5218, 3213, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5217, 3213, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5216, 3213, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5215, 3213, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5214, 3213, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5213, 3213, 'isDefault', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5212, 3213, 'environmentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5211, 3213, 'url', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5210, 3213, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5209, 3213, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5208, 3207, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5207, 3207, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5206, 3207, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5205, 3207, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5204, 3207, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5203, 3207, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5202, 3207, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5201, 3207, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5200, 3207, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5199, 3207, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5198, 3207, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5197, 3207, 'ancestors', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5196, 3207, 'parentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5195, 3207, 'type', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5194, 3207, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5193, 3207, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5192, 3197, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5191, 3197, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5190, 3197, 'globalHeaders', '[{\'description\': \'内容类型\', \'is_run\': True, \'key\': \'Content-Type\', \'value\': \'application/json\'}]', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5189, 3197, 'requestTimeout', '5000', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5188, 3197, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5187, 3197, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5186, 3197, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5185, 3197, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5184, 3197, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5183, 3197, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5182, 3197, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5181, 3197, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5180, 3197, 'isDefault', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5179, 3197, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5178, 3197, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5177, 3197, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5176, 3187, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5175, 3187, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5174, 3187, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5173, 3187, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5172, 3187, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5171, 3187, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5170, 3187, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5169, 3187, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5168, 3187, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5167, 3187, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5166, 3187, 'projectId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5165, 3187, 'password', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5164, 3187, 'username', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5163, 3187, 'port', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5162, 3187, 'host', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5161, 3187, 'dbType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5160, 3187, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5159, 3187, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5158, 3181, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5157, 3181, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5156, 3181, 'ancestors', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5155, 3181, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5154, 3181, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5153, 3181, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5152, 3181, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5151, 3181, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5150, 3181, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5149, 3181, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5148, 3181, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5147, 3181, 'parentId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5146, 3181, 'type', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5144, 3181, 'id', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5145, 3181, 'name', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5143, 3162, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5142, 3153, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5141, 3153, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5140, 3153, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5139, 3153, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5138, 3153, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5137, 3153, 'exceptionInfo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5136, 3153, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5135, 3153, 'jobMessage', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5134, 3153, 'jobTrigger', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5133, 3153, 'jobKwargs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5132, 3153, 'jobArgs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5131, 3153, 'invokeTarget', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5130, 3153, 'jobExecutor', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5129, 3153, 'jobGroup', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5128, 3153, 'jobName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5127, 3153, 'jobLogId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5126, 3149, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5125, 3149, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5124, 3149, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5123, 3149, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5122, 3149, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5121, 3149, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5120, 3149, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5119, 3149, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5118, 3149, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5117, 3149, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5116, 3149, 'concurrent', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5115, 3149, 'misfirePolicy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5114, 3149, 'cronExpression', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5113, 3149, 'jobKwargs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5112, 3149, 'jobArgs', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5111, 3149, 'invokeTarget', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5110, 3149, 'jobExecutor', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5109, 3149, 'jobGroup', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5108, 3149, 'jobName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5107, 3149, 'jobId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5106, 3139, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5105, 3139, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5104, 3139, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5103, 3139, 'sortNo', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5102, 3139, 'description', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5101, 3139, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5100, 3139, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5099, 3139, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5098, 3139, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5097, 3139, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5096, 3139, 'bizTag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5095, 3139, 'fileHash', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5094, 3139, 'isTemp', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5093, 3139, 'storageType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5092, 3139, 'fileUrl', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5091, 3139, 'filePath', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5090, 3139, 'fileSize', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5089, 3139, 'mimeType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5088, 3139, 'fileExt', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5087, 3139, 'storedName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5086, 3139, 'originalName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5085, 3139, 'fileId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5084, 3132, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5083, 3131, 'files', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5082, 3130, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5081, 3130, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5080, 3130, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5079, 3130, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5078, 3130, 'isAsc', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5077, 3130, 'orderByColumn', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5076, 3130, 'loginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5075, 3130, 'msg', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5074, 3130, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5073, 3130, 'os', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5072, 3130, 'browser', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5071, 3130, 'loginLocation', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5070, 3130, 'ipaddr', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5069, 3130, 'userName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5068, 3130, 'infoId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5067, 3125, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5066, 3125, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5065, 3125, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5064, 3125, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5063, 3125, 'isAsc', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5062, 3125, 'orderByColumn', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5061, 3125, 'costTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5060, 3125, 'operTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5059, 3125, 'errorMsg', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5058, 3125, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5057, 3125, 'jsonResult', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5056, 3125, 'operParam', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5055, 3125, 'operLocation', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5054, 3125, 'operIp', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5053, 3125, 'operUrl', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5052, 3125, 'deptName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5051, 3125, 'operName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5050, 3125, 'operatorType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5049, 3125, 'requestMethod', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5048, 3125, 'method', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5047, 3125, 'businessType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5046, 3125, 'title', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5045, 3125, 'operId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5044, 3116, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5043, 3116, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5042, 3116, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5041, 3116, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5040, 3116, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5039, 3116, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5038, 3116, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5037, 3116, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5036, 3116, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5035, 3116, 'configType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5034, 3116, 'configValue', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5033, 3116, 'configKey', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5032, 3116, 'configName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5031, 3116, 'configId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5030, 3108, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5029, 3108, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5028, 3108, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5027, 3108, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5026, 3108, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5025, 3108, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5024, 3108, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5023, 3108, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5022, 3108, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5021, 3108, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5020, 3108, 'isDefault', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5019, 3108, 'listClass', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5018, 3108, 'cssClass', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5017, 3108, 'dictType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5016, 3108, 'dictValue', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5015, 3108, 'dictLabel', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5014, 3108, 'dictSort', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5013, 3108, 'dictCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5012, 3101, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5011, 3101, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5010, 3101, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5009, 3101, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5008, 3101, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5007, 3101, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5006, 3101, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5005, 3101, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5004, 3101, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5003, 3101, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5002, 3101, 'dictType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5001, 3101, 'dictName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (5000, 3101, 'dictId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4999, 3093, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4998, 3093, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4997, 3093, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4996, 3093, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4995, 3093, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4994, 3093, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4993, 3093, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4992, 3093, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4991, 3093, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4990, 3093, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4989, 3093, 'postSort', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4988, 3093, 'postName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4987, 3093, 'postCode', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4986, 3093, 'postId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4985, 3068, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4984, 3068, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4983, 3068, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4982, 3068, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4981, 3068, 'admin', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4980, 3068, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4979, 3068, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4978, 3068, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4977, 3068, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4976, 3068, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4975, 3068, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4974, 3068, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4973, 3068, 'deptCheckStrictly', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4972, 3068, 'menuCheckStrictly', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4971, 3068, 'dataScope', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4970, 3068, 'roleSort', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4969, 3068, 'roleKey', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4968, 3068, 'roleName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4967, 3068, 'roleId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4966, 3058, 'pageSize', '10', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4965, 3058, 'pageNum', '1', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4964, 3058, 'endTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4963, 3058, 'beginTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4962, 3058, 'admin', 'False', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4961, 3058, 'remark', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4960, 3058, 'updateTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4959, 3058, 'updateBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4958, 3058, 'createTime', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4957, 3058, 'createBy', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4956, 3058, 'loginDate', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4955, 3058, 'loginIp', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4954, 3058, 'delFlag', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4953, 3058, 'status', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4952, 3058, 'password', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4951, 3058, 'avatar', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4950, 3058, 'sex', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4949, 3058, 'phonenumber', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4948, 3058, 'email', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4947, 3058, 'userType', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4946, 3058, 'nickName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4945, 3058, 'userName', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4944, 3058, 'deptId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4943, 3058, 'userId', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4942, 3056, 'file', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4941, 3054, 'avatarfile', '', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, NULL, 1, 0);
INSERT INTO `api_formdata` VALUES (4940, 3037, 'login_info', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4939, 3037, 'uuid', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4938, 3037, 'code', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4937, 3037, 'client_secret', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4936, 3037, 'client_id', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4935, 3037, 'scope', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4934, 3037, 'password', 'admin123', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4933, 3037, 'username', 'admin', 1, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);
INSERT INTO `api_formdata` VALUES (4932, 3037, 'grant_type', '', 0, 0, 'STRING', '[]', '', '2025-12-31 14:44:26', 'admin', '2025-12-31 14:47:37', NULL, '', 1, 0);

-- ----------------------------
-- Table structure for api_headers
-- ----------------------------
DROP TABLE IF EXISTS `api_headers`;
CREATE TABLE `api_headers`  (
  `header_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `case_id` int(11) NOT NULL COMMENT '关联的测试用例ID',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '请求头键名',
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求头值',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用该请求头',
  `is_required` tinyint(1) NULL DEFAULT NULL COMMENT '是否必填参数',
  `data_type` enum('STRING','INTEGER','BOOLEAN','NUMBER','ARRAY','FILE') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据类型',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`header_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 7574 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口请求头表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_headers
-- ----------------------------

-- ----------------------------
-- Table structure for api_notification
-- ----------------------------
DROP TABLE IF EXISTS `api_notification`;
CREATE TABLE `api_notification`  (
  `notification_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '通知ID',
  `user_id` bigint(20) NOT NULL COMMENT '接收用户ID',
  `notification_type` enum('SUCCESS','ERROR','ALERT') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '通知类型(system/task/workflow/alert)',
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '通知标题',
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '通知内容',
  `is_read` tinyint(1) NULL DEFAULT NULL COMMENT '是否已读',
  `read_time` datetime NULL DEFAULT NULL COMMENT '阅读时间',
  `business_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关联业务类型(workflow/test_case/report等)',
  `business_id` bigint(20) NULL DEFAULT NULL COMMENT '关联业务ID',
  `extra_data` json NULL COMMENT '扩展数据',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`notification_id`) USING BTREE,
  INDEX `ix_notification_is_read`(`is_read`) USING BTREE,
  INDEX `ix_notification_type`(`notification_type`) USING BTREE,
  INDEX `ix_notification_user_id`(`user_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3781 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '通知消息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_notification
-- ----------------------------

-- ----------------------------
-- Table structure for api_param_item
-- ----------------------------
DROP TABLE IF EXISTS `api_param_item`;
CREATE TABLE `api_param_item`  (
  `key_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `parameterization_id` bigint(20) NULL DEFAULT NULL COMMENT '所属参数表ID',
  `group_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参数分组',
  `key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参数键',
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '参数值',
  `item` json NULL COMMENT '节点配置信息',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`key_id`) USING BTREE,
  INDEX `ix_param_item_table_id`(`parameterization_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3910 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '参数化数据表行' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_param_item
-- ----------------------------

-- ----------------------------
-- Table structure for api_param_table
-- ----------------------------
DROP TABLE IF EXISTS `api_param_table`;
CREATE TABLE `api_param_table`  (
  `parameterization_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `workflow_id` bigint(20) NULL DEFAULT NULL COMMENT '所属执行器ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参数表名称',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`parameterization_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1912 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '参数化数据表主表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_param_table
-- ----------------------------

-- ----------------------------
-- Table structure for api_params
-- ----------------------------
DROP TABLE IF EXISTS `api_params`;
CREATE TABLE `api_params`  (
  `param_id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `case_id` int(11) NOT NULL COMMENT '关联的测试用例ID',
  `key` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '参数键名',
  `value` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '参数值',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用该参数',
  `is_required` tinyint(1) NULL DEFAULT NULL COMMENT '是否必填参数',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `data_type` enum('STRING','INTEGER','BOOLEAN','NUMBER','ARRAY','FILE') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据类型',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`param_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 7942 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口请求参数表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_params
-- ----------------------------
INSERT INTO `api_params` VALUES (7941, 3663, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7940, 3663, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7939, 3663, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7938, 3663, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7937, 3663, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7936, 3663, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7935, 3663, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7934, 3663, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7933, 3663, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7932, 3663, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7931, 3663, 'status', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7921, 3659, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7920, 3659, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7919, 3659, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7918, 3659, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7917, 3659, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7916, 3659, 'businessId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7915, 3659, 'businessType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7914, 3659, 'readTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7913, 3659, 'isRead', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7912, 3659, 'message', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7911, 3659, 'title', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7910, 3659, 'notificationType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7909, 3659, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7908, 3659, 'notificationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7907, 3656, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7906, 3656, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7905, 3656, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7904, 3656, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7903, 3656, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7902, 3656, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7901, 3656, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7900, 3656, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7899, 3656, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7898, 3656, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7897, 3656, 'businessId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7896, 3656, 'businessType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7895, 3656, 'readTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7894, 3656, 'isRead', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7893, 3656, 'message', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7892, 3656, 'title', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7891, 3656, 'notificationType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7890, 3656, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7889, 3656, 'notificationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7888, 3649, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7887, 3649, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7886, 3649, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7885, 3649, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7884, 3649, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7883, 3649, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7882, 3649, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7881, 3649, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7880, 3649, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7879, 3649, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7878, 3649, 'triggerType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7877, 3649, 'isSuccess', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7876, 3649, 'duration', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7875, 3649, 'failedCases', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7874, 3649, 'successCases', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7873, 3649, 'totalCases', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7872, 3649, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7871, 3649, 'startTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7870, 3649, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7869, 3649, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7868, 3649, 'reportId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7867, 3643, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7866, 3643, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7865, 3643, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7864, 3643, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7863, 3643, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7862, 3643, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7861, 3643, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7860, 3643, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7859, 3643, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7858, 3643, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7857, 3643, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7856, 3643, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7855, 3643, 'groupName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7854, 3643, 'parameterizationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7853, 3643, 'keyId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7852, 3641, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7851, 3641, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7850, 3641, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7849, 3641, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7848, 3641, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7847, 3641, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7846, 3641, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7845, 3641, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7844, 3641, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7843, 3641, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7842, 3641, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7841, 3641, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7840, 3641, 'parameterizationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7839, 3637, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7838, 3637, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7837, 3637, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7836, 3637, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7835, 3637, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7834, 3637, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7833, 3637, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7832, 3637, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7831, 3637, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7830, 3637, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7829, 3637, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7828, 3637, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7827, 3637, 'parameterizationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7826, 3628, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7825, 3628, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7824, 3628, 'eventType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7823, 3628, 'reportId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7822, 3628, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7821, 3628, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7820, 3628, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7819, 3628, 'method', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7818, 3628, 'delFlag', '0', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7817, 3628, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7816, 3628, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7815, 3628, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7814, 3628, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7813, 3628, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7812, 3628, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7811, 3628, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7810, 3628, 'assertionSuccess', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7809, 3628, 'responseTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7808, 3628, 'responseStatusCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7807, 3628, 'isSuccess', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7806, 3628, 'executionTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7805, 3628, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7804, 3628, 'logId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7788, 3620, 'nodeId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7787, 3614, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7786, 3614, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7785, 3614, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7784, 3614, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7783, 3614, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7782, 3614, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7781, 3614, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7780, 3614, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7779, 3614, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7778, 3614, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7768, 3614, 'nodeId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7763, 3608, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7762, 3608, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7761, 3608, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7760, 3608, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7759, 3608, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7758, 3608, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7757, 3608, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7756, 3608, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7755, 3608, 'errorMessage', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7754, 3608, 'skippedNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7753, 3608, 'failedNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7752, 3608, 'successNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7751, 3608, 'totalNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7750, 3608, 'duration', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7745, 3608, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7739, 3601, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7738, 3601, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7737, 3601, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7736, 3601, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7735, 3601, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7734, 3601, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7733, 3601, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7732, 3601, 'parentSubmoduleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7731, 3601, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7730, 3601, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7729, 3600, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7728, 3600, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7727, 3600, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7726, 3600, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7725, 3600, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7724, 3600, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7723, 3600, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7722, 3600, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7721, 3600, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7720, 3600, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7719, 3600, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7718, 3600, 'parentSubmoduleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7717, 3600, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7716, 3600, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7715, 3599, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7714, 3599, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7713, 3599, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7712, 3599, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7711, 3599, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7710, 3599, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7709, 3599, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7708, 3599, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7707, 3599, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7706, 3599, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7705, 3599, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7704, 3599, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7703, 3599, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7702, 3599, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7701, 3599, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7700, 3599, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7699, 3593, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7698, 3593, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7697, 3593, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7696, 3593, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7695, 3593, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7694, 3593, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7693, 3593, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7692, 3593, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7691, 3593, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7690, 3593, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7689, 3593, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7688, 3593, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7687, 3593, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7686, 3593, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7685, 3593, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7684, 3593, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7683, 3593, 'formdataId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7682, 3587, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7681, 3587, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7680, 3587, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7679, 3587, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7678, 3587, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7677, 3587, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7676, 3587, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7675, 3587, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7674, 3587, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7673, 3587, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7672, 3587, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7671, 3587, 'waitTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7670, 3587, 'script', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7669, 3587, 'dbOperation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7668, 3587, 'databaseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7667, 3587, 'responseCookie', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7666, 3587, 'responseHeader', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7665, 3587, 'xpathExpression', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7664, 3587, 'regularExpression', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7663, 3587, 'variableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7662, 3587, 'extractIndexIsRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7661, 3587, 'extractIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7660, 3587, 'jsonpath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7659, 3587, 'extractVariableMethod', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7658, 3587, 'teardownType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7657, 3587, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7656, 3587, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7655, 3587, 'teardownId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7654, 3581, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7653, 3581, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7652, 3581, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7651, 3581, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7650, 3581, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7649, 3581, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7648, 3581, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7647, 3581, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7646, 3581, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7645, 3581, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7644, 3581, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7643, 3581, 'extractIndexIsRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7642, 3581, 'extractIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7641, 3581, 'waitTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7640, 3581, 'variableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7639, 3581, 'jsonpath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7638, 3581, 'script', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7637, 3581, 'dbConnectionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7636, 3581, 'setupType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7635, 3581, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7634, 3581, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7633, 3581, 'setupId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7632, 3575, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7631, 3575, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7630, 3575, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7629, 3575, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7628, 3575, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7627, 3575, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7626, 3575, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7625, 3575, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7624, 3575, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7623, 3575, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7622, 3575, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7621, 3575, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7620, 3575, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7619, 3575, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7618, 3575, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7617, 3575, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7616, 3575, 'paramId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7615, 3569, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7614, 3569, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7613, 3569, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7612, 3569, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7611, 3569, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7610, 3569, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7609, 3569, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7608, 3569, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7607, 3569, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7606, 3569, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7605, 3569, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7604, 3569, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7603, 3569, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7602, 3569, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7601, 3569, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7600, 3569, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7599, 3569, 'headerId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7598, 3563, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7597, 3563, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7596, 3563, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7595, 3563, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7594, 3563, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7593, 3563, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7592, 3563, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7591, 3563, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7590, 3563, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7589, 3563, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7588, 3563, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7587, 3563, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7586, 3563, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7585, 3563, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7584, 3563, 'domain', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7583, 3563, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7582, 3563, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7581, 3563, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7580, 3563, 'cookieId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7579, 3557, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7578, 3557, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7577, 3557, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7576, 3557, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7575, 3557, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7574, 3557, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7573, 3557, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7572, 3557, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7571, 3557, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7570, 3557, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7569, 3557, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7568, 3557, 'assertType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7567, 3557, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7566, 3557, 'assertionMethod', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7565, 3557, 'extractIndexIsRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7564, 3557, 'jsonpathIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7563, 3557, 'jsonpath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7562, 3557, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7561, 3557, 'assertionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7560, 3540, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7559, 3540, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7558, 3540, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7557, 3540, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7556, 3540, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7555, 3540, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7554, 3540, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7553, 3540, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7552, 3540, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7551, 3540, 'sleep', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7550, 3540, 'statusCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7549, 3540, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7548, 3540, 'requestType', 'NONE', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7547, 3540, 'method', 'GET', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7546, 3540, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7545, 3540, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7544, 3540, 'parentSubmoduleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7543, 3540, 'parentCaseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7542, 3540, 'copyId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7541, 3540, 'caseType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7518, 3527, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7517, 3527, 'isDefault', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7516, 3527, 'environmentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7515, 3527, 'url', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7514, 3527, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7513, 3527, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7512, 3522, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7511, 3522, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7510, 3522, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7509, 3522, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7508, 3522, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7507, 3522, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7506, 3522, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7505, 3522, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7504, 3522, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7503, 3522, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7502, 3522, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7501, 3522, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7500, 3522, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7499, 3522, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7498, 3522, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7497, 3522, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7496, 3519, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7495, 3519, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7494, 3519, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7493, 3519, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7492, 3519, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7491, 3519, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7490, 3519, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7489, 3519, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7488, 3519, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7487, 3519, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7486, 3519, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7485, 3519, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7484, 3519, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7483, 3519, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7482, 3519, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7481, 3519, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7480, 3518, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7479, 3518, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7478, 3518, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7477, 3518, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7476, 3518, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7475, 3518, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7474, 3518, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7473, 3518, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7472, 3518, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7471, 3518, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7470, 3518, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7469, 3518, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7450, 3517, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7449, 3517, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7448, 3512, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7447, 3512, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7446, 3512, 'requestTimeout', '5000', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7445, 3512, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7444, 3512, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7443, 3512, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7442, 3512, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7441, 3512, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7440, 3512, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7439, 3512, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7438, 3512, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7437, 3512, 'isDefault', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7436, 3512, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7435, 3512, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7434, 3512, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7433, 3509, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7432, 3509, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7431, 3509, 'requestTimeout', '5000', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7430, 3509, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7429, 3509, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7428, 3509, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7427, 3509, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7426, 3509, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7425, 3509, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7424, 3509, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7423, 3509, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7422, 3509, 'isDefault', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7421, 3509, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7420, 3509, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7419, 3509, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7418, 3501, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7417, 3501, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7416, 3501, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7415, 3501, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7414, 3501, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7413, 3501, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7412, 3501, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7411, 3501, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7410, 3501, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7409, 3501, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7408, 3501, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7407, 3501, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7406, 3501, 'username', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7405, 3501, 'port', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7404, 3501, 'host', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7403, 3501, 'dbType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7402, 3501, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7401, 3501, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7400, 3495, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7399, 3495, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7398, 3495, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7397, 3495, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7396, 3495, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7395, 3495, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7394, 3495, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7393, 3495, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7392, 3495, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7391, 3495, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7390, 3495, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7389, 3495, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7388, 3495, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7387, 3495, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7386, 3495, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7385, 3490, 'tables', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7384, 3489, 'sql', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7383, 3486, 'tables', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7382, 3485, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7381, 3485, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7380, 3485, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7379, 3485, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7378, 3485, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7377, 3485, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7376, 3485, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7375, 3485, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7374, 3485, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7373, 3485, 'options', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7372, 3485, 'genPath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7371, 3485, 'functionAuthor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7370, 3485, 'functionName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7369, 3485, 'businessName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7368, 3485, 'moduleName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7367, 3485, 'packageName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7366, 3485, 'tplWebType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7365, 3485, 'tplCategory', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7364, 3485, 'className', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7363, 3485, 'subTableFkName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7362, 3485, 'subTableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7361, 3485, 'tableComment', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7360, 3485, 'tableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7359, 3485, 'tableId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7358, 3484, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7357, 3484, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7356, 3484, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7355, 3484, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7351, 3484, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7350, 3484, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7349, 3484, 'options', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7347, 3484, 'functionAuthor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7348, 3484, 'genPath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7346, 3484, 'functionName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7345, 3484, 'businessName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7342, 3484, 'tplWebType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7343, 3484, 'packageName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7344, 3484, 'moduleName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7341, 3484, 'tplCategory', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7340, 3484, 'className', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7339, 3484, 'subTableFkName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7338, 3484, 'subTableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7337, 3484, 'tableComment', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7336, 3484, 'tableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7335, 3484, 'tableId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7334, 3483, 'resource', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7333, 3482, 'delete', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7468, 3518, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7467, 3518, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7466, 3518, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7465, 3518, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7464, 3517, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7463, 3517, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7462, 3517, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7461, 3517, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7460, 3517, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7459, 3517, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7458, 3517, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7457, 3517, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7456, 3517, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7455, 3517, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7454, 3517, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7453, 3517, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7452, 3517, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7451, 3517, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7332, 3482, 'fileName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7331, 3469, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7330, 3469, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7328, 3469, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7329, 3469, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7326, 3469, 'exceptionInfo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7327, 3469, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7325, 3469, 'jobMessage', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7324, 3469, 'jobTrigger', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7323, 3469, 'jobKwargs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7322, 3469, 'jobArgs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7321, 3469, 'invokeTarget', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7320, 3469, 'jobExecutor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7319, 3469, 'jobGroup', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7318, 3469, 'jobName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7354, 3484, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7353, 3484, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7352, 3484, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7317, 3469, 'jobLogId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7316, 3461, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7315, 3461, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7314, 3461, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7312, 3461, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7313, 3461, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7311, 3461, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7310, 3461, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7309, 3461, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7308, 3461, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7307, 3461, 'cronExpression', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7306, 3461, 'jobKwargs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7305, 3461, 'jobArgs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7304, 3461, 'invokeTarget', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7303, 3461, 'jobExecutor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7302, 3461, 'jobGroup', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7300, 3461, 'jobId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7301, 3461, 'jobName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7299, 3459, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7298, 3459, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7296, 3459, 'os', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7297, 3459, 'loginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7295, 3459, 'browser', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7294, 3459, 'loginLocation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7293, 3459, 'ipaddr', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7292, 3459, 'deptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7291, 3459, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7290, 3459, 'tokenId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7289, 3453, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7288, 3453, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7286, 3453, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7287, 3453, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7284, 3453, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7285, 3453, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7283, 3453, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7282, 3453, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7281, 3453, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7279, 3453, 'bizTag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7280, 3453, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7278, 3453, 'fileHash', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7277, 3453, 'isTemp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7276, 3453, 'storageType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7275, 3453, 'fileUrl', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7274, 3453, 'filePath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7273, 3453, 'fileSize', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7272, 3453, 'mimeType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7271, 3453, 'fileExt', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7270, 3453, 'storedName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7269, 3453, 'originalName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7268, 3453, 'fileId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7267, 3451, 'custom_path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7266, 3451, 'file_type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7265, 3450, 'filename', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7264, 3450, 'file_type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7263, 3445, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7262, 3445, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7261, 3445, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7260, 3445, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7259, 3445, 'orderByColumn', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7258, 3445, 'loginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7257, 3445, 'msg', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7256, 3445, 'os', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7255, 3445, 'browser', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7254, 3445, 'loginLocation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7253, 3445, 'ipaddr', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7252, 3445, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7251, 3445, 'infoId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7250, 3441, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7249, 3441, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7248, 3441, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7247, 3441, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7749, 3608, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7748, 3608, 'startTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7747, 3608, 'status', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7746, 3608, 'workflowName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7744, 3608, 'workflowExecutionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7743, 3601, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7742, 3601, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7741, 3601, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7740, 3601, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7246, 3441, 'orderByColumn', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7245, 3441, 'costTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7244, 3441, 'operTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7243, 3441, 'errorMsg', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7242, 3441, 'jsonResult', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7241, 3441, 'operParam', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7240, 3441, 'operLocation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7239, 3441, 'operIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7238, 3441, 'operUrl', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7237, 3441, 'deptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7236, 3441, 'operName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7235, 3441, 'requestMethod', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7234, 3441, 'method', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7233, 3441, 'title', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7232, 3441, 'operId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7231, 3436, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7230, 3436, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7229, 3436, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7227, 3436, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7228, 3436, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7226, 3436, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7225, 3436, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7224, 3436, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7223, 3436, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7222, 3436, 'noticeContent', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7777, 3614, 'createdAt', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7776, 3614, 'retryCount', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7775, 3614, 'errorMessage', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7774, 3614, 'conditionResult', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7773, 3614, 'loopIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7772, 3614, 'duration', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7771, 3614, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7770, 3614, 'startTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7769, 3614, 'status', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7767, 3614, 'workflowExecutionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7766, 3614, 'nodeExecutionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7765, 3608, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7764, 3608, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7803, 3620, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7802, 3620, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7801, 3620, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7800, 3620, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7799, 3620, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7798, 3620, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7797, 3620, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7796, 3620, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7795, 3620, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7794, 3620, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7793, 3620, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7792, 3620, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7791, 3620, 'name', '未命名', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7790, 3620, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7789, 3620, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7221, 3436, 'noticeTitle', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7220, 3436, 'noticeId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7219, 3428, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7218, 3428, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7217, 3428, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7216, 3428, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7215, 3428, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7214, 3428, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7213, 3428, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7212, 3428, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7211, 3428, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7210, 3428, 'configValue', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7209, 3428, 'configKey', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7208, 3428, 'configName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7207, 3428, 'configId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7206, 3422, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7205, 3422, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7204, 3422, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7203, 3422, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7202, 3422, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7201, 3422, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7200, 3422, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7199, 3422, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7198, 3422, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7197, 3422, 'listClass', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7196, 3422, 'cssClass', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7195, 3422, 'dictType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7194, 3422, 'dictValue', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7193, 3422, 'dictLabel', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7192, 3422, 'dictSort', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7191, 3422, 'dictCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7190, 3413, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7189, 3413, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7188, 3413, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7187, 3413, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7186, 3413, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7185, 3413, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7184, 3413, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7183, 3413, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7182, 3413, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7181, 3413, 'dictType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7180, 3413, 'dictName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7179, 3413, 'dictId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7178, 3407, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7177, 3407, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7176, 3407, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7175, 3407, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7174, 3407, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7173, 3407, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7172, 3407, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7171, 3407, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7170, 3407, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7169, 3407, 'postSort', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7168, 3407, 'postName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7167, 3407, 'postCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7166, 3407, 'postId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7165, 3402, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7164, 3402, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7163, 3402, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7162, 3402, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7161, 3402, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7160, 3402, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7159, 3402, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7158, 3402, 'phone', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7157, 3402, 'leader', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7156, 3402, 'orderNum', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7155, 3402, 'deptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7154, 3402, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7153, 3402, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7152, 3402, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7151, 3396, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7150, 3396, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7149, 3396, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7148, 3396, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7147, 3396, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7146, 3396, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7145, 3396, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7144, 3396, 'icon', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7143, 3396, 'perms', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7142, 3396, 'routeName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7141, 3396, 'query', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7140, 3396, 'component', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7139, 3396, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7138, 3396, 'orderNum', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7137, 3396, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7136, 3396, 'menuName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7135, 3396, 'menuId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7134, 3393, 'roleIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7133, 3393, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7132, 3393, 'userIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7131, 3393, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7130, 3391, 'roleIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7129, 3391, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7128, 3391, 'userIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7127, 3391, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7126, 3390, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7125, 3390, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7124, 3390, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7123, 3390, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7122, 3390, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7121, 3390, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7120, 3390, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7119, 3390, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7118, 3390, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7117, 3390, 'loginDate', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7116, 3390, 'loginIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7115, 3390, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7114, 3390, 'avatar', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7113, 3390, 'phonenumber', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7112, 3390, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7111, 3390, 'userType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7110, 3390, 'nickName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7109, 3390, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7108, 3390, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7107, 3390, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7106, 3389, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7104, 3389, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7105, 3389, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7103, 3389, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7102, 3389, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7101, 3389, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7100, 3389, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7099, 3389, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7098, 3389, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7097, 3389, 'loginDate', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7096, 3389, 'loginIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7093, 3389, 'phonenumber', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7094, 3389, 'avatar', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7095, 3389, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7092, 3389, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7091, 3389, 'userType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7090, 3389, 'nickName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7089, 3389, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7088, 3389, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7087, 3389, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7086, 3381, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7084, 3381, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7083, 3381, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7081, 3381, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7080, 3381, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7079, 3381, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7078, 3381, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7076, 3381, 'deptCheckStrictly', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7075, 3381, 'menuCheckStrictly', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7085, 3381, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7082, 3381, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7077, 3381, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7074, 3381, 'roleSort', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7073, 3381, 'roleKey', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7072, 3381, 'roleName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7071, 3381, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7069, 3379, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7068, 3375, 'updateSupport', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7063, 3363, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7070, 3379, 'roleIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7067, 3371, 'user_id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7066, 3363, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7065, 3363, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7064, 3363, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7062, 3363, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7061, 3363, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7060, 3363, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7059, 3363, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7058, 3363, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7057, 3363, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7056, 3363, 'loginDate', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7055, 3363, 'loginIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7054, 3363, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7053, 3363, 'avatar', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7052, 3363, 'phonenumber', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7051, 3363, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7050, 3363, 'userType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7049, 3363, 'nickName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7540, 3540, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7539, 3533, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7538, 3533, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7537, 3533, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7536, 3533, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7535, 3533, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7534, 3533, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7533, 3533, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7532, 3533, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7531, 3533, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7530, 3533, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7529, 3533, 'sourceType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7528, 3533, 'environmentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7527, 3527, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7526, 3527, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7525, 3527, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7524, 3527, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7523, 3527, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7522, 3527, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7521, 3527, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7520, 3527, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7519, 3527, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7930, 3663, 'scriptContent', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7929, 3663, 'scriptType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7928, 3663, 'scriptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7927, 3663, 'scriptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7926, 3659, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7925, 3659, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7924, 3659, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7923, 3659, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7922, 3659, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7048, 3363, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7047, 3363, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7046, 3363, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7045, 3344, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7044, 3344, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7043, 3344, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7042, 3344, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7041, 3344, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7040, 3344, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7039, 3344, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7038, 3344, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7037, 3344, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7036, 3344, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7035, 3344, 'status', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7034, 3344, 'scriptContent', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7013, 3340, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7033, 3344, 'scriptType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7032, 3344, 'scriptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7031, 3344, 'scriptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7030, 3340, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7029, 3340, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7028, 3340, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7027, 3340, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7026, 3340, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7025, 3340, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7024, 3340, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7023, 3340, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7022, 3340, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7021, 3340, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7020, 3340, 'businessId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7019, 3340, 'businessType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7018, 3340, 'readTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7017, 3340, 'isRead', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7016, 3340, 'message', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7015, 3340, 'title', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7014, 3340, 'notificationType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7012, 3340, 'notificationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7011, 3337, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7010, 3337, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7008, 3337, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7009, 3337, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7007, 3337, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7006, 3337, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7005, 3337, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7004, 3337, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7003, 3337, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7002, 3337, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7001, 3337, 'businessId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6999, 3337, 'readTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (7000, 3337, 'businessType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6998, 3337, 'isRead', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6997, 3337, 'message', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6996, 3337, 'title', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6994, 3337, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6995, 3337, 'notificationType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6993, 3337, 'notificationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6992, 3330, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6991, 3330, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6989, 3330, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6990, 3330, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6988, 3330, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6987, 3330, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6986, 3330, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6984, 3330, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6985, 3330, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6983, 3330, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6982, 3330, 'triggerType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6981, 3330, 'isSuccess', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6980, 3330, 'duration', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6979, 3330, 'failedCases', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6977, 3330, 'totalCases', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6978, 3330, 'successCases', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6976, 3330, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6975, 3330, 'startTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6974, 3330, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6972, 3330, 'reportId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6973, 3330, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6971, 3324, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6970, 3324, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6969, 3324, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6967, 3324, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6968, 3324, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6966, 3324, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6965, 3324, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6963, 3324, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6964, 3324, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6961, 3324, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6962, 3324, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6960, 3324, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6959, 3324, 'groupName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6958, 3324, 'parameterizationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6956, 3322, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6957, 3324, 'keyId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6955, 3322, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6954, 3322, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6953, 3322, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6951, 3322, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6952, 3322, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6950, 3322, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6949, 3322, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6947, 3322, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6948, 3322, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6946, 3322, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6945, 3322, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6944, 3322, 'parameterizationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6942, 3318, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6943, 3318, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6940, 3318, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6941, 3318, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6939, 3318, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6938, 3318, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6937, 3318, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6935, 3318, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6936, 3318, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6934, 3318, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6933, 3318, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6932, 3318, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:30', '', '2025-12-31 14:44:30', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6930, 3309, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6931, 3318, 'parameterizationId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6929, 3309, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6928, 3309, 'eventType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6926, 3309, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6927, 3309, 'reportId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6924, 3309, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6925, 3309, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6923, 3309, 'method', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6922, 3309, 'delFlag', '0', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6921, 3309, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6919, 3309, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6920, 3309, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6918, 3309, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6917, 3309, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6915, 3309, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6916, 3309, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6914, 3309, 'assertionSuccess', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6913, 3309, 'responseTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6912, 3309, 'responseStatusCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6910, 3309, 'executionTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6911, 3309, 'isSuccess', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6908, 3309, 'logId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6909, 3309, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6907, 3301, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6906, 3301, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6905, 3301, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6903, 3301, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6904, 3301, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6902, 3301, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6901, 3301, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6900, 3301, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6898, 3301, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6899, 3301, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6897, 3301, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6896, 3301, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6895, 3301, 'name', '未命名', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6894, 3301, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6893, 3301, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6892, 3301, 'nodeId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6891, 3295, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6890, 3295, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6889, 3295, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6888, 3295, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6887, 3295, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6886, 3295, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6885, 3295, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6884, 3295, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6883, 3295, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6882, 3295, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6881, 3295, 'createdAt', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6880, 3295, 'retryCount', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6879, 3295, 'errorMessage', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6878, 3295, 'conditionResult', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6877, 3295, 'loopIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6876, 3295, 'duration', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6875, 3295, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6874, 3295, 'startTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6873, 3295, 'status', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6872, 3295, 'nodeId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6871, 3295, 'workflowExecutionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6870, 3295, 'nodeExecutionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6869, 3289, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6868, 3289, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6867, 3289, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6866, 3289, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6865, 3289, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6864, 3289, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6863, 3289, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6862, 3289, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6861, 3289, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6860, 3289, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6859, 3289, 'errorMessage', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6858, 3289, 'skippedNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6857, 3289, 'failedNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6856, 3289, 'successNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6855, 3289, 'totalNodes', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6854, 3289, 'duration', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6853, 3289, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6852, 3289, 'startTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6851, 3289, 'status', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6850, 3289, 'workflowName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6849, 3289, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6848, 3289, 'workflowExecutionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6847, 3282, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6846, 3282, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6845, 3282, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6844, 3282, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6843, 3282, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6842, 3282, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6841, 3282, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6840, 3282, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6839, 3282, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6838, 3282, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6837, 3282, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6836, 3282, 'parentSubmoduleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6835, 3282, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6834, 3282, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6833, 3281, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6832, 3281, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6831, 3281, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6830, 3281, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6829, 3281, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6828, 3281, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6827, 3281, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6826, 3281, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6825, 3281, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6824, 3281, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6823, 3281, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6822, 3281, 'parentSubmoduleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6821, 3281, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6820, 3281, 'workflowId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6819, 3280, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6818, 3280, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6817, 3280, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6816, 3280, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6815, 3280, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6814, 3280, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6813, 3280, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6812, 3280, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6811, 3280, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6810, 3280, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6809, 3280, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6808, 3280, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6807, 3280, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6806, 3280, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6805, 3280, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6804, 3280, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6803, 3274, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6802, 3274, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6801, 3274, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6800, 3274, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6799, 3274, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6798, 3274, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6797, 3274, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6796, 3274, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6795, 3274, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6794, 3274, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6793, 3274, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6792, 3274, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6791, 3274, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6790, 3274, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6789, 3274, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6788, 3274, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6787, 3274, 'formdataId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6786, 3268, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6785, 3268, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6784, 3268, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6783, 3268, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6782, 3268, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6781, 3268, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6780, 3268, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6779, 3268, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6778, 3268, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6777, 3268, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6776, 3268, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6775, 3268, 'waitTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6774, 3268, 'script', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6773, 3268, 'dbOperation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6772, 3268, 'databaseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6771, 3268, 'responseCookie', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6770, 3268, 'responseHeader', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6769, 3268, 'xpathExpression', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6768, 3268, 'regularExpression', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6767, 3268, 'variableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6766, 3268, 'extractIndexIsRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6765, 3268, 'extractIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6764, 3268, 'jsonpath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6763, 3268, 'extractVariableMethod', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6762, 3268, 'teardownType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6761, 3268, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6760, 3268, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6759, 3268, 'teardownId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6758, 3262, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6757, 3262, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6756, 3262, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6755, 3262, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6754, 3262, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6753, 3262, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6752, 3262, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6751, 3262, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6750, 3262, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6749, 3262, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6748, 3262, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6747, 3262, 'extractIndexIsRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6746, 3262, 'extractIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6745, 3262, 'waitTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6744, 3262, 'variableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6743, 3262, 'jsonpath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6742, 3262, 'script', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6741, 3262, 'dbConnectionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6740, 3262, 'setupType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6739, 3262, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6738, 3262, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6737, 3262, 'setupId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6736, 3256, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6735, 3256, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6734, 3256, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6733, 3256, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6732, 3256, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6731, 3256, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6730, 3256, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6729, 3256, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6728, 3256, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6727, 3256, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6726, 3256, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6725, 3256, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6724, 3256, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6723, 3256, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6722, 3256, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6721, 3256, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6720, 3256, 'paramId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6719, 3250, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6718, 3250, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:29', '', '2025-12-31 14:44:29', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6717, 3250, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6716, 3250, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6715, 3250, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6714, 3250, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6713, 3250, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6712, 3250, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6711, 3250, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6710, 3250, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6709, 3250, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6708, 3250, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6707, 3250, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6706, 3250, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6705, 3250, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6704, 3250, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6703, 3250, 'headerId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6702, 3244, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6701, 3244, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6700, 3244, 'dataType', 'string', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6699, 3244, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6698, 3244, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6697, 3244, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6696, 3244, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6695, 3244, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6694, 3244, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6693, 3244, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6692, 3244, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6691, 3244, 'isRequired', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6690, 3244, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6689, 3244, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6688, 3244, 'domain', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6687, 3244, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6686, 3244, 'key', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6685, 3244, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6684, 3244, 'cookieId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6683, 3238, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6682, 3238, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6681, 3238, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6680, 3238, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6679, 3238, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6678, 3238, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6677, 3238, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6676, 3238, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6675, 3238, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6674, 3238, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6673, 3238, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6672, 3238, 'assertType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6671, 3238, 'value', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6670, 3238, 'assertionMethod', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6669, 3238, 'extractIndexIsRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6668, 3238, 'jsonpathIndex', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6667, 3238, 'jsonpath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6666, 3238, 'caseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6665, 3238, 'assertionId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6664, 3221, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6663, 3221, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6662, 3221, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6661, 3221, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6660, 3221, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6659, 3221, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6658, 3221, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6657, 3221, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6656, 3221, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6655, 3221, 'sleep', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6654, 3221, 'statusCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6653, 3221, 'isRun', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6652, 3221, 'requestType', 'NONE', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6651, 3221, 'method', 'GET', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6650, 3221, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6649, 3221, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6648, 3221, 'parentSubmoduleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6647, 3221, 'parentCaseId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6646, 3221, 'copyId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6645, 3221, 'caseType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6644, 3221, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6643, 3214, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6642, 3214, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6641, 3214, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6640, 3214, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6639, 3214, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6638, 3214, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6637, 3214, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6636, 3214, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6635, 3214, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6634, 3214, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6633, 3214, 'sourceType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6632, 3214, 'environmentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6631, 3208, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6630, 3208, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6629, 3208, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6628, 3208, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6627, 3208, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6626, 3208, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6625, 3208, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6624, 3208, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6623, 3208, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6622, 3208, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6621, 3208, 'isDefault', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6620, 3208, 'environmentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6619, 3208, 'url', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6618, 3208, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6617, 3208, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6616, 3203, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6615, 3203, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6614, 3203, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6613, 3203, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6612, 3203, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6611, 3203, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6610, 3203, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6609, 3203, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6608, 3203, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6607, 3203, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6606, 3203, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6605, 3203, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6604, 3203, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6603, 3203, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6602, 3203, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6601, 3203, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6600, 3200, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6599, 3200, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6598, 3200, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6597, 3200, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6596, 3200, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6595, 3200, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6594, 3200, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6593, 3200, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6592, 3200, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6591, 3200, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6590, 3200, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6589, 3200, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6588, 3200, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6587, 3200, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6586, 3200, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6585, 3200, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6584, 3199, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6583, 3199, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6582, 3199, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6581, 3199, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6580, 3199, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6579, 3199, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6578, 3199, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6577, 3199, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6576, 3199, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6575, 3199, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6574, 3199, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6573, 3199, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6572, 3199, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6571, 3199, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6570, 3199, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6569, 3199, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6568, 3198, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6567, 3198, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6566, 3198, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6565, 3198, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6564, 3198, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6563, 3198, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6562, 3198, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6561, 3198, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6560, 3198, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6559, 3198, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6558, 3198, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6557, 3198, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6556, 3198, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6555, 3198, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6554, 3198, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6553, 3198, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6552, 3193, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6551, 3193, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6550, 3193, 'requestTimeout', '5000', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6549, 3193, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6548, 3193, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6547, 3193, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6546, 3193, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6545, 3193, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6544, 3193, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6543, 3193, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6542, 3193, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6541, 3193, 'isDefault', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6540, 3193, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6539, 3193, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6538, 3193, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6537, 3190, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6536, 3190, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6535, 3190, 'requestTimeout', '5000', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6534, 3190, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6533, 3190, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6532, 3190, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6531, 3190, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6530, 3190, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6529, 3190, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6528, 3190, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6527, 3190, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6526, 3190, 'isDefault', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6525, 3190, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6524, 3190, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6523, 3190, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:28', '', '2025-12-31 14:44:28', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6522, 3182, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6521, 3182, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6520, 3182, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6519, 3182, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6518, 3182, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6517, 3182, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6516, 3182, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6515, 3182, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6514, 3182, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6513, 3182, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6512, 3182, 'projectId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6511, 3182, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6510, 3182, 'username', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6509, 3182, 'port', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6508, 3182, 'host', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6507, 3182, 'dbType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6506, 3182, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6505, 3182, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6504, 3176, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6503, 3176, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6502, 3176, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6501, 3176, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6500, 3176, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6499, 3176, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6498, 3176, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6497, 3176, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6496, 3176, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6495, 3176, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6494, 3176, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6493, 3176, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6492, 3176, 'type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6491, 3176, 'name', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6490, 3176, 'id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6489, 3171, 'tables', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6488, 3170, 'sql', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6487, 3167, 'tables', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6486, 3166, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6485, 3166, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6484, 3166, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6483, 3166, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6482, 3166, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6481, 3166, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6480, 3166, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6479, 3166, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6478, 3166, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6477, 3166, 'options', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6476, 3166, 'genPath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6475, 3166, 'functionAuthor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6474, 3166, 'functionName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6473, 3166, 'businessName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6472, 3166, 'moduleName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6471, 3166, 'packageName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6470, 3166, 'tplWebType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6469, 3166, 'tplCategory', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6468, 3166, 'className', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6467, 3166, 'subTableFkName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6466, 3166, 'subTableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6465, 3166, 'tableComment', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6464, 3166, 'tableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6463, 3166, 'tableId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6462, 3165, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6461, 3165, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6460, 3165, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6459, 3165, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6458, 3165, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6457, 3165, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6456, 3165, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6455, 3165, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6454, 3165, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6453, 3165, 'options', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6452, 3165, 'genPath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6451, 3165, 'functionAuthor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6450, 3165, 'functionName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6449, 3165, 'businessName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6448, 3165, 'moduleName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6447, 3165, 'packageName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6446, 3165, 'tplWebType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6445, 3165, 'tplCategory', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6444, 3165, 'className', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6443, 3165, 'subTableFkName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6442, 3165, 'subTableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6441, 3165, 'tableComment', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6440, 3165, 'tableName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6439, 3165, 'tableId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6438, 3164, 'resource', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6437, 3163, 'delete', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6436, 3163, 'fileName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6435, 3150, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6434, 3150, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6433, 3150, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6432, 3150, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6431, 3150, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6430, 3150, 'exceptionInfo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6429, 3150, 'jobMessage', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6428, 3150, 'jobTrigger', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6427, 3150, 'jobKwargs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6426, 3150, 'jobArgs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6425, 3150, 'invokeTarget', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6424, 3150, 'jobExecutor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6423, 3150, 'jobGroup', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6422, 3150, 'jobName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6421, 3150, 'jobLogId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6420, 3142, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6419, 3142, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6418, 3142, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6417, 3142, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6416, 3142, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6415, 3142, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6414, 3142, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6413, 3142, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6412, 3142, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6411, 3142, 'cronExpression', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6410, 3142, 'jobKwargs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6409, 3142, 'jobArgs', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6408, 3142, 'invokeTarget', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6407, 3142, 'jobExecutor', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6406, 3142, 'jobGroup', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6405, 3142, 'jobName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6404, 3142, 'jobId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6403, 3140, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6402, 3140, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6401, 3140, 'loginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6400, 3140, 'os', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6399, 3140, 'browser', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6398, 3140, 'loginLocation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6397, 3140, 'ipaddr', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6396, 3140, 'deptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6395, 3140, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6394, 3140, 'tokenId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6393, 3134, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6392, 3134, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6391, 3134, 'delFlag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6390, 3134, 'sortNo', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6389, 3134, 'description', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6388, 3134, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6387, 3134, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6386, 3134, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6385, 3134, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6384, 3134, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6383, 3134, 'bizTag', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6382, 3134, 'fileHash', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6381, 3134, 'isTemp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6380, 3134, 'storageType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6379, 3134, 'fileUrl', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6378, 3134, 'filePath', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6377, 3134, 'fileSize', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6376, 3134, 'mimeType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6375, 3134, 'fileExt', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6374, 3134, 'storedName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6373, 3134, 'originalName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6372, 3134, 'fileId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6371, 3132, 'custom_path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6370, 3132, 'file_type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6369, 3131, 'filename', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6368, 3131, 'file_type', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6367, 3126, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6366, 3126, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6365, 3126, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6364, 3126, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6363, 3126, 'orderByColumn', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6362, 3126, 'loginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6361, 3126, 'msg', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6360, 3126, 'os', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6359, 3126, 'browser', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6358, 3126, 'loginLocation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6357, 3126, 'ipaddr', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6356, 3126, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6355, 3126, 'infoId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6354, 3122, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6353, 3122, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6352, 3122, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6351, 3122, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6350, 3122, 'orderByColumn', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6349, 3122, 'costTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6348, 3122, 'operTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6347, 3122, 'errorMsg', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6346, 3122, 'jsonResult', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6345, 3122, 'operParam', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6344, 3122, 'operLocation', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6343, 3122, 'operIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6342, 3122, 'operUrl', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6341, 3122, 'deptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6340, 3122, 'operName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6339, 3122, 'requestMethod', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6338, 3122, 'method', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6337, 3122, 'title', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6336, 3122, 'operId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6335, 3117, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6334, 3117, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6333, 3117, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6332, 3117, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6331, 3117, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6330, 3117, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6329, 3117, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6328, 3117, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6327, 3117, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6326, 3117, 'noticeContent', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6325, 3117, 'noticeTitle', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6324, 3117, 'noticeId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6323, 3109, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6322, 3109, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6321, 3109, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6320, 3109, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6319, 3109, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6318, 3109, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6317, 3109, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6316, 3109, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6315, 3109, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6314, 3109, 'configValue', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6313, 3109, 'configKey', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6312, 3109, 'configName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6311, 3109, 'configId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:27', '', '2025-12-31 14:44:27', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6310, 3103, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6309, 3103, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6308, 3103, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6307, 3103, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6306, 3103, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6305, 3103, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6304, 3103, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6303, 3103, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6302, 3103, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6301, 3103, 'listClass', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6300, 3103, 'cssClass', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6299, 3103, 'dictType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6298, 3103, 'dictValue', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6297, 3103, 'dictLabel', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6296, 3103, 'dictSort', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6295, 3103, 'dictCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6294, 3094, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6293, 3094, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6292, 3094, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6291, 3094, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6290, 3094, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6289, 3094, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6288, 3094, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6287, 3094, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6286, 3094, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6285, 3094, 'dictType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6284, 3094, 'dictName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6283, 3094, 'dictId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6282, 3088, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6281, 3088, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6280, 3088, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6279, 3088, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6278, 3088, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6277, 3088, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6276, 3088, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6275, 3088, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6274, 3088, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6273, 3088, 'postSort', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6272, 3088, 'postName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6271, 3088, 'postCode', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6270, 3088, 'postId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6269, 3083, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6268, 3083, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6267, 3083, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6266, 3083, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6265, 3083, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6264, 3083, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6263, 3083, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6262, 3083, 'phone', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6261, 3083, 'leader', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6260, 3083, 'orderNum', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6259, 3083, 'deptName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6258, 3083, 'ancestors', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6257, 3083, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6256, 3083, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6255, 3077, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6254, 3077, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6253, 3077, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6252, 3077, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6251, 3077, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6250, 3077, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6249, 3077, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6248, 3077, 'icon', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6247, 3077, 'perms', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6246, 3077, 'routeName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6245, 3077, 'query', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6244, 3077, 'component', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6243, 3077, 'path', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6242, 3077, 'orderNum', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6241, 3077, 'parentId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6240, 3077, 'menuName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6239, 3077, 'menuId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6238, 3074, 'roleIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6237, 3074, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6236, 3074, 'userIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6235, 3074, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6234, 3072, 'roleIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6233, 3072, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6232, 3072, 'userIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6231, 3072, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6230, 3071, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6229, 3071, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6228, 3071, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6227, 3071, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6226, 3071, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6225, 3071, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6224, 3071, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6223, 3071, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6222, 3071, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6221, 3071, 'loginDate', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6220, 3071, 'loginIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6219, 3071, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6218, 3071, 'avatar', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6217, 3071, 'phonenumber', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6216, 3071, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6215, 3071, 'userType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6214, 3071, 'nickName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6213, 3071, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6212, 3071, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6211, 3071, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6210, 3070, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6209, 3070, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6208, 3070, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6207, 3070, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6206, 3070, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6205, 3070, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6204, 3070, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6203, 3070, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6202, 3070, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6201, 3070, 'loginDate', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6200, 3070, 'loginIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6199, 3070, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6198, 3070, 'avatar', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6197, 3070, 'phonenumber', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6196, 3070, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6195, 3070, 'userType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6194, 3070, 'nickName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6193, 3070, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6192, 3070, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6191, 3070, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6190, 3062, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6189, 3062, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6188, 3062, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6187, 3062, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6186, 3062, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6185, 3062, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6184, 3062, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6183, 3062, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6182, 3062, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6181, 3062, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6180, 3062, 'deptCheckStrictly', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6179, 3062, 'menuCheckStrictly', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6178, 3062, 'roleSort', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6177, 3062, 'roleKey', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6176, 3062, 'roleName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6175, 3062, 'roleId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6174, 3060, 'roleIds', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6173, 3060, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6172, 3056, 'updateSupport', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6171, 3052, 'user_id', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6170, 3044, 'pageSize', '10', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6169, 3044, 'pageNum', '1', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6168, 3044, 'endTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6167, 3044, 'beginTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6166, 3044, 'admin', 'False', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6165, 3044, 'remark', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6164, 3044, 'updateTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6163, 3044, 'updateBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6162, 3044, 'createTime', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6161, 3044, 'createBy', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6160, 3044, 'loginDate', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6159, 3044, 'loginIp', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6158, 3044, 'password', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6157, 3044, 'avatar', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6156, 3044, 'phonenumber', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6155, 3044, 'email', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6154, 3044, 'userType', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6153, 3044, 'nickName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6152, 3044, 'userName', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6151, 3044, 'deptId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);
INSERT INTO `api_params` VALUES (6150, 3044, 'userId', '', 1, 1, NULL, 'STRING', '', '2025-12-31 14:44:26', '', '2025-12-31 14:44:26', NULL, 1, 0);

-- ----------------------------
-- Table structure for api_project
-- ----------------------------
DROP TABLE IF EXISTS `api_project`;
CREATE TABLE `api_project`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '项目名称',
  `type` enum('0','1','2','3') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '项目类型',
  `parent_id` bigint(20) NULL DEFAULT NULL COMMENT '父部门id',
  `ancestors` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '祖级列表',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 48 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '项目表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_project
-- ----------------------------
INSERT INTO `api_project` VALUES (1, 'CaseGo', NULL, NULL, NULL, 'admin', '2025-08-01 09:20:36', 'admin', '2025-08-26 13:47:40', NULL, NULL, NULL, 0);
INSERT INTO `api_project` VALUES (46, '测试项目', NULL, NULL, NULL, 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, NULL, 0);
INSERT INTO `api_project` VALUES (47, 'test', NULL, NULL, NULL, 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, NULL, 0);

-- ----------------------------
-- Table structure for api_project_submodules
-- ----------------------------
DROP TABLE IF EXISTS `api_project_submodules`;
CREATE TABLE `api_project_submodules`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模块名称',
  `type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模块类型',
  `parent_id` bigint(20) NULL DEFAULT NULL COMMENT '父id',
  `ancestors` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '祖级列表',
  `project_id` bigint(20) NULL DEFAULT NULL COMMENT '所属项目id',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_submodules_parent`(`parent_id`) USING BTREE,
  INDEX `idx_submodules_project_type`(`project_id`, `type`, `del_flag`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 361 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '项目模块表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_project_submodules
-- ----------------------------
INSERT INTO `api_project_submodules` VALUES (330, '系统监控-定时任务', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 2, 0);
INSERT INTO `api_project_submodules` VALUES (331, '系统监控-菜单管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 3, 0);
INSERT INTO `api_project_submodules` VALUES (332, '系统监控-缓存监控', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 4, 0);
INSERT INTO `api_project_submodules` VALUES (333, '通用模块', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 5, 0);
INSERT INTO `api_project_submodules` VALUES (334, '代码生成', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 6, 0);
INSERT INTO `api_project_submodules` VALUES (335, '项目模块', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 7, 0);
INSERT INTO `api_project_submodules` VALUES (336, '数据库模块', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 8, 0);
INSERT INTO `api_project_submodules` VALUES (337, '环境模块', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 9, 0);
INSERT INTO `api_project_submodules` VALUES (338, '项目子模块', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 10, 0);
INSERT INTO `api_project_submodules` VALUES (339, '环境服务表', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:34', NULL, NULL, 11, 0);
INSERT INTO `api_project_submodules` VALUES (340, '环境緩存變量表', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:34', NULL, NULL, 12, 0);
INSERT INTO `api_project_submodules` VALUES (341, '测试接口', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:34', NULL, NULL, 13, 0);
INSERT INTO `api_project_submodules` VALUES (342, '接口断言', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:34', NULL, NULL, 14, 0);
INSERT INTO `api_project_submodules` VALUES (343, '接口请求Cookie', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:35', NULL, NULL, 15, 0);
INSERT INTO `api_project_submodules` VALUES (344, '接口请求头', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:35', NULL, NULL, 16, 0);
INSERT INTO `api_project_submodules` VALUES (345, '接口请求参数', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:35', NULL, NULL, 17, 0);
INSERT INTO `api_project_submodules` VALUES (346, '接口前置操作', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:35', NULL, NULL, 18, 0);
INSERT INTO `api_project_submodules` VALUES (347, '接口后置操作', '1', NULL, NULL, 1, '', '2025-12-31 14:49:56', 'admin', '2025-12-31 14:50:35', NULL, NULL, 19, 0);
INSERT INTO `api_project_submodules` VALUES (348, '接口的bodyfrom表单', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 20, 0);
INSERT INTO `api_project_submodules` VALUES (349, '工作流基础信息', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 21, 0);
INSERT INTO `api_project_submodules` VALUES (317, '登录模块', '1', NULL, NULL, 1, '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:50:34', NULL, NULL, 1, 0);
INSERT INTO `api_project_submodules` VALUES (359, '公共脚本', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 22, 0);
INSERT INTO `api_project_submodules` VALUES (360, 'Faker配置', '1', NULL, NULL, 1, '', '2025-12-31 14:49:58', 'admin', '2025-12-31 14:50:35', NULL, NULL, 23, 0);
INSERT INTO `api_project_submodules` VALUES (357, 'WebSocket 路由', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 24, 0);
INSERT INTO `api_project_submodules` VALUES (355, '工作流参数表横向', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 25, 0);
INSERT INTO `api_project_submodules` VALUES (354, '工作流参数表', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 26, 0);
INSERT INTO `api_project_submodules` VALUES (358, '通知消息', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 27, 0);
INSERT INTO `api_project_submodules` VALUES (356, '工作流报告', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 28, 0);
INSERT INTO `api_project_submodules` VALUES (352, '工作流节点', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 29, 0);
INSERT INTO `api_project_submodules` VALUES (353, '接口执行日志', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 30, 0);
INSERT INTO `api_project_submodules` VALUES (350, '工作流执行日志', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 31, 0);
INSERT INTO `api_project_submodules` VALUES (351, '工作节点执行日志', '1', NULL, NULL, 1, '', '2025-12-31 14:49:57', 'admin', '2025-12-31 14:50:35', NULL, NULL, 32, 0);
INSERT INTO `api_project_submodules` VALUES (329, '系统监控-在线用户', '1', NULL, NULL, 1, '', '2025-12-31 14:49:55', 'admin', '2025-12-31 14:50:35', NULL, NULL, 33, 0);
INSERT INTO `api_project_submodules` VALUES (327, '系统管理-日志管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 34, 0);
INSERT INTO `api_project_submodules` VALUES (328, '系统管理-附件管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 35, 0);
INSERT INTO `api_project_submodules` VALUES (326, '系统管理-通知公告管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 36, 0);
INSERT INTO `api_project_submodules` VALUES (324, '系统管理-字典管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 37, 0);
INSERT INTO `api_project_submodules` VALUES (325, '系统管理-参数管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 38, 0);
INSERT INTO `api_project_submodules` VALUES (323, '系统管理-岗位管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 39, 0);
INSERT INTO `api_project_submodules` VALUES (322, '系统管理-部门管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 40, 0);
INSERT INTO `api_project_submodules` VALUES (321, '系统管理-菜单管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 41, 0);
INSERT INTO `api_project_submodules` VALUES (320, '系统管理-角色管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:54', 'admin', '2025-12-31 14:50:35', NULL, NULL, 42, 0);
INSERT INTO `api_project_submodules` VALUES (319, '系统管理-用户管理', '1', NULL, NULL, 1, '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:50:35', NULL, NULL, 43, 0);
INSERT INTO `api_project_submodules` VALUES (318, '验证码模块', '1', NULL, NULL, 1, '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:50:35', NULL, NULL, 44, 0);

-- ----------------------------
-- Table structure for api_script_library
-- ----------------------------
DROP TABLE IF EXISTS `api_script_library`;
CREATE TABLE `api_script_library`  (
  `script_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '脚本ID',
  `script_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '脚本名称',
  `script_type` enum('python','javascript') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '脚本类型(python/javascript)',
  `script_content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '脚本内容',
  `status` int(11) NULL DEFAULT NULL COMMENT '状态(0停用 1正常)',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`script_id`) USING BTREE,
  INDEX `ix_script_library_name`(`script_name`) USING BTREE,
  INDEX `ix_script_library_type`(`script_type`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '公共脚本库' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_script_library
-- ----------------------------
INSERT INTO `api_script_library` VALUES (3, NULL, 'python', 'print(111)\nprint(redis)\nprint(db)\nprint(await set_cache(\"demo\",999))\nprint(await get_cache(\"demo\"))', 1, 'admin', '2025-12-14 21:57:00', 'admin', '2025-12-14 21:57:00', NULL, NULL, 1, 1);
INSERT INTO `api_script_library` VALUES (2, '测试脚本12222222222', 'python', 'print(redis)\nprint(db)\nprint(await set_cache(\"测试公共脚本\",999111111111111))\nprint(await get_cache(\"测试公共脚本\"))\nprint(logger)', 1, 'guest', '2025-12-13 18:06:12', 'admin', '2025-12-24 14:20:51', NULL, NULL, 1, 0);
INSERT INTO `api_script_library` VALUES (4, NULL, 'python', 'print(111)\nprint(redis)\nprint(db)\nprint(await set_cache(\"demo\",999))\nprint(await get_cache(\"demo\"))', 1, 'admin', '2025-12-14 21:57:02', 'admin', '2025-12-14 21:57:02', NULL, NULL, 1, 1);
INSERT INTO `api_script_library` VALUES (5, 'demo2', 'python', '222333', 1, 'admin', '2025-12-16 09:24:09', 'admin', '2025-12-18 18:05:50', NULL, NULL, 1, 0);
INSERT INTO `api_script_library` VALUES (6, '测试124', 'python', '', 1, 'admin', '2025-12-22 11:58:28', 'admin', '2025-12-22 11:58:28', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for api_services
-- ----------------------------
DROP TABLE IF EXISTS `api_services`;
CREATE TABLE `api_services`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '服务ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '服务名称',
  `url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '服务地址',
  `environment_id` int(11) NOT NULL COMMENT '所属环境ID',
  `is_default` tinyint(1) NOT NULL COMMENT '是否为默认服务',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 69 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '环境服务地址表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_services
-- ----------------------------
INSERT INTO `api_services` VALUES (1, 'demo1', 'www.baidu.com', 6, 0, 'admin', '2025-08-01 17:37:52', 'admin', '2025-08-01 12:27:32', NULL, NULL, NULL, 0);
INSERT INTO `api_services` VALUES (2, '百度地址', 'www.baidu.com', 1, 0, 'admin', '2025-08-01 17:39:40', 'admin', '2025-09-12 03:28:39', NULL, NULL, NULL, 1);
INSERT INTO `api_services` VALUES (16, '434312413', '41341234', 38, 1, 'admin', '2025-08-01 23:10:08', 'admin', '2025-08-01 23:10:08', NULL, NULL, NULL, 0);
INSERT INTO `api_services` VALUES (17, '123', '123123', 31, 0, 'guest', '2025-08-02 09:07:15', 'guest', '2025-08-02 09:07:15', NULL, NULL, NULL, 0);
INSERT INTO `api_services` VALUES (18, '123123', '123123', 30, 0, 'guest', '2025-08-02 09:07:59', 'admin', '2025-08-02 22:09:11', NULL, NULL, NULL, 0);
INSERT INTO `api_services` VALUES (19, '123123', '123123123', 1, 0, 'admin', '2025-08-02 20:13:36', 'guest', '2025-09-12 03:28:39', NULL, NULL, NULL, 1);
INSERT INTO `api_services` VALUES (20, '123123', '123123', 30, 0, 'admin', '2025-08-02 22:07:15', 'admin', '2025-08-02 22:09:10', NULL, NULL, NULL, 0);
INSERT INTO `api_services` VALUES (21, '123123', '123123', 30, 1, 'admin', '2025-08-02 22:07:28', 'admin', '2025-08-02 22:09:08', NULL, NULL, NULL, 0);
INSERT INTO `api_services` VALUES (22, '的点点滴滴的点点滴滴哒哒哒哒哒哒哒哒哒', 'https://www.baidu.com', 2, 0, 'guest', '2025-08-03 21:44:12', 'admin', '2025-11-27 16:58:52', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (23, '啊撒大声地', 'http://127.0.0.1:9099', 3, 1, 'admin', '2025-08-05 22:09:25', 'admin', '2025-12-31 14:51:40', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (24, '阿斯顿撒打算', 'http://127.0.0.1:9099', 2, 1, 'admin', '2025-08-05 22:09:58', 'admin', '2025-12-31 14:51:31', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (25, '演示环境服务地址', 'https://demo.1592653.xyz/dev-api/', 4, 1, 'admin', '2025-08-05 22:10:06', 'admin', '2025-12-23 11:10:40', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (26, 'demo01', 'http://127.0.0.1:9099', 1, 1, 'admin', '2025-08-07 21:28:28', 'admin', '2025-12-05 14:07:58', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (27, '啊实打实大师', '阿萨德阿萨德', 54, 1, 'admin', '2025-08-07 21:47:43', 'admin', '2025-08-07 21:47:43', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (28, '888', '3333', 54, 0, 'admin', '2025-08-07 21:54:15', 'admin', '2025-08-07 13:54:25', NULL, NULL, 1, 1);
INSERT INTO `api_services` VALUES (29, '默認服務', NULL, 129, 1, 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (30, '默認服務', NULL, 130, 1, 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (31, '默認服務', NULL, 131, 1, 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (32, '默認服務', NULL, 132, 1, 'admin', '2025-08-07 22:23:31', 'admin', '2025-08-07 22:23:31', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (33, '默認服務', NULL, 133, 1, 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (34, '默認服務', NULL, 134, 1, 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (35, '默認服務', NULL, 135, 1, 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (36, '默認服務', NULL, 136, 1, 'admin', '2025-08-09 00:15:41', 'admin', '2025-08-09 00:15:41', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (37, '默認服務', NULL, 137, 1, 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (38, '默認服務', NULL, 138, 1, 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (39, '默認服務', NULL, 139, 1, 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (40, '默認服務', NULL, 140, 1, 'david', '2025-08-10 19:26:27', 'david', '2025-08-10 19:26:27', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (41, '默認服務', NULL, 141, 1, 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (42, '默認服務', NULL, 142, 1, 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (43, '默認服務', NULL, 143, 1, 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (44, '默認服務', NULL, 144, 1, 'admin', '2025-08-15 14:29:14', 'admin', '2025-08-15 14:29:14', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (45, '默認服務', NULL, 145, 1, 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:13:29', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (46, '默認服務', NULL, 146, 1, 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:13:29', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (47, '默認服務', NULL, 147, 1, 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:13:29', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (48, '默認服務', NULL, 148, 1, 'guest', '2025-08-19 17:13:29', 'guest', '2025-08-19 17:13:29', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (49, '默認服務', '', 150, 1, 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (50, '默認服務', '', 151, 1, 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (51, '默認服務', '', 152, 1, 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (52, '默認服務', '', 153, 1, 'guest', '2025-08-20 12:38:08', 'guest', '2025-08-20 12:38:08', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (53, '默認服務', ' ', 154, 1, 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (54, '默認服務', ' ', 155, 1, 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (55, '默認服務', ' ', 156, 1, 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (56, '默認服務', ' ', 157, 1, 'guest', '2025-08-20 12:41:02', 'guest', '2025-08-20 12:41:02', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (57, '默認服務', ' ', 158, 1, 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (58, '默認服務', ' ', 159, 1, 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (59, '默認服務', ' ', 160, 1, 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (60, '默認服務', ' ', 161, 1, 'admin', '2025-08-21 13:36:24', 'admin', '2025-08-21 13:36:24', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (61, '默認服務', ' ', 162, 1, 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (62, '默認服務', ' ', 163, 1, 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (63, '默認服務', ' ', 164, 1, 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (64, '默認服務', ' ', 165, 1, 'admin', '2025-08-29 11:56:49', 'admin', '2025-08-29 11:56:49', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (65, '默認服務', ' ', 167, 1, 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (66, '默認服務', ' ', 168, 1, 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (67, '默認服務', ' ', 169, 1, 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);
INSERT INTO `api_services` VALUES (68, '默認服務', ' ', 170, 1, 'dawei', '2025-10-31 16:29:48', 'dawei', '2025-10-31 16:29:48', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for api_setup
-- ----------------------------
DROP TABLE IF EXISTS `api_setup`;
CREATE TABLE `api_setup`  (
  `setup_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作名称',
  `case_id` int(11) NOT NULL COMMENT '关联的测试用例ID',
  `setup_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作类型 (db_connection, execute_script, wait_time)',
  `db_connection_id` int(11) NULL DEFAULT NULL COMMENT '数据库连接ID',
  `script` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '脚本语句',
  `extract_variables` json NULL COMMENT '提取额外参数的KEY-VALUE',
  `jsonpath` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'jsonpath提取表达式',
  `variable_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '变量名称（用于存储提取的数据）',
  `wait_time` int(11) NULL DEFAULT NULL COMMENT '等待时间（毫秒）',
  `extract_index` int(11) NULL DEFAULT NULL COMMENT '提取索引',
  `extract_index_is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否执行提取索引操作',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否执行该前置操作',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`setup_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 4932 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口前置操作表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_setup
-- ----------------------------

-- ----------------------------
-- Table structure for api_teardown
-- ----------------------------
DROP TABLE IF EXISTS `api_teardown`;
CREATE TABLE `api_teardown`  (
  `teardown_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '操作ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作名称',
  `case_id` int(11) NOT NULL COMMENT '关联的测试用例ID',
  `teardown_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '操作类型 (extract_variable, db_operation, custom_script, wait_time)',
  `extract_variable_method` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '提取响应的方法： response_textresponse_jsonresponse_xmlresponse_headerresponse_cookie',
  `jsonpath` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT 'jsonpath提取表达式（用于提取变量）',
  `extract_variables` json NULL COMMENT '提取额外参数的KEY-VALUE',
  `extract_index` int(11) NULL DEFAULT NULL COMMENT '提取索引',
  `extract_index_is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否执行提取索引操作',
  `regular_expression` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '正则表达式（用于提取text）',
  `xpath_expression` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '正则表达式（用于提取xml）',
  `response_header` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '正则表达式（用于提取响应头）',
  `response_cookie` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '正则表达式（用于提取cookie）',
  `variable_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '变量名称（用于存储提取的数据）',
  `database_id` int(11) NULL DEFAULT NULL COMMENT '数据库连接ID',
  `db_operation` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '数据库操作语句（用于数据库操作）',
  `script` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '自定义脚本语句（用于自定义脚本）',
  `wait_time` int(11) NULL DEFAULT NULL COMMENT '等待时间（毫秒，用于等待时间）',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否执行该后置操作',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`teardown_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 6031 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口后置操作表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_teardown
-- ----------------------------
INSERT INTO `api_teardown` VALUES (6030, '提取token', 3356, 'EXTRACT_VARIABLE', 'response_json', '$.token', '[{\"jsonpath\": null, \"variable_name\": null}]', 0, 0, '', '', '', '', 'token', NULL, '', '', 0, 1, 'admin', '2025-12-31 14:52:10', 'admin', '2025-12-31 14:52:29', NULL, NULL, 1, 0);
INSERT INTO `api_teardown` VALUES (6029, '提取token', 3037, 'EXTRACT_VARIABLE', 'response_json', '$.token', '[{\"jsonpath\": null, \"variable_name\": null}]', 0, 0, '', '', '', '', 'token', NULL, '', '', 0, 1, 'admin', '2025-12-31 14:47:18', 'admin', '2025-12-31 14:47:37', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for api_test_cases
-- ----------------------------
DROP TABLE IF EXISTS `api_test_cases`;
CREATE TABLE `api_test_cases`  (
  `case_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '测试用例ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '测试用例名称',
  `case_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '测试用例类型',
  `copy_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '复制用例ID',
  `parent_case_id` int(11) NULL DEFAULT NULL COMMENT '父级测试接口ID',
  `project_id` int(11) NULL DEFAULT NULL COMMENT '项目ID',
  `parent_submodule_id` bigint(20) NULL DEFAULT NULL COMMENT '父级模块ID',
  `path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求路径',
  `method` enum('POST','GET','PUT','DELETE','OPTIONS','HEAD','PATCH','TRACE','CONNECT','COPY','LINK','UNLINK','PURGE','LOCK','UNLOCK','MKCOL','MOVE','PROPFIND','REPORT','VIEW') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求方法',
  `request_type` enum('NONE','Form_Data','x_www_form_urlencoded','JSON','XML','Raw','Binary') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '请求类型',
  `json_data` json NULL COMMENT '请求json，xml，raw数据',
  `is_run` smallint(6) NULL DEFAULT NULL COMMENT '是否执行',
  `status_code` int(11) NULL DEFAULT NULL COMMENT '预期状态码',
  `sleep` int(11) NULL DEFAULT NULL COMMENT '执行前等待时间',
  `case_file_config` json NULL COMMENT '用例的文件配置',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  `response_example` json NULL COMMENT '返回示例',
  PRIMARY KEY (`case_id`) USING BTREE,
  INDEX `idx_cases_parent_type`(`parent_case_id`, `case_type`, `del_flag`) USING BTREE,
  INDEX `idx_cases_project`(`project_id`, `del_flag`) USING BTREE,
  INDEX `idx_cases_submodule_type`(`parent_submodule_id`, `case_type`, `del_flag`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3675 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口用例表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_test_cases
-- ----------------------------
INSERT INTO `api_test_cases` VALUES (3673, '测试执行函数', '1', NULL, NULL, 1, 360, '/api_testing/faker_config/test', 'POST', 'JSON', '{\"args\": [\"\"], \"function_name\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3674, '获取所有可用函数列表', '1', NULL, NULL, 1, 360, '/api_testing/faker_config/functions', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3672, '保存自定义 Faker 配置', '1', NULL, NULL, 1, 360, '/api_testing/faker_config/save', 'POST', 'JSON', '{\"content\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3669, 'Execute Script', '1', NULL, NULL, 1, 359, '/api_script_library/script_library/debug', 'POST', 'JSON', '{\"envId\": 0, \"scriptId\": \"\", \"scriptType\": \"\", \"scriptContent\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3670, '获取自定义 Faker 配置', '1', NULL, NULL, 1, 360, '/api_testing/faker_config/content', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3671, '校验代码语法', '1', NULL, NULL, 1, 360, '/api_testing/faker_config/validate', 'POST', 'JSON', '{\"content\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3666, 'Delete Api Script Library Script Library', '1', NULL, NULL, 1, 359, '/api_script_library/script_library/{script_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3667, 'Query Detail Api Script Library Script Library', '1', NULL, NULL, 1, 359, '/api_script_library/script_library/{script_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3668, 'Export Api Script Library Script Library List', '1', NULL, NULL, 1, 359, '/api_script_library/script_library/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3665, 'Edit Api Script Library Script Library', '1', NULL, NULL, 1, 359, '/api_script_library/script_library', 'PUT', 'JSON', '{\"remark\": \"\", \"sortNo\": \"\", \"status\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"scriptId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"scriptName\": \"\", \"scriptType\": \"\", \"updateTime\": \"\", \"description\": \"\", \"scriptContent\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3664, 'Add Api Script Library Script Library', '1', NULL, NULL, 1, 359, '/api_script_library/script_library', 'POST', 'JSON', '{\"remark\": \"\", \"sortNo\": \"\", \"status\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"scriptId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"scriptName\": \"\", \"scriptType\": \"\", \"updateTime\": \"\", \"description\": \"\", \"scriptContent\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:58', '', '2025-12-31 14:49:58', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3663, 'Get Api Script Library Script Library List', '1', NULL, NULL, 1, 359, '/api_script_library/script_library/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3661, 'Query Detail Task Notification Notification', '1', NULL, NULL, 1, 358, '/task_notification/notification/{notification_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3662, 'Export Task Notification Notification List', '1', NULL, NULL, 1, 358, '/task_notification/notification/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3660, 'Delete Task Notification Notification', '1', NULL, NULL, 1, 358, '/task_notification/notification/{notification_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3658, 'Edit Task Notification Notification', '1', NULL, NULL, 1, 358, '/task_notification/notification', 'PUT', 'JSON', '{\"title\": \"\", \"isRead\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"message\": \"\", \"createBy\": \"\", \"readTime\": \"\", \"updateBy\": \"\", \"extraData\": \"\", \"businessId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"businessType\": \"\", \"notificationId\": \"\", \"notificationType\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3659, 'Edit Task Notification Notification', '1', NULL, NULL, 1, 358, '/task_notification/notification/readall', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3656, 'Get Task Notification Notification List', '1', NULL, NULL, 1, 358, '/task_notification/notification/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3657, 'Add Task Notification Notification', '1', NULL, NULL, 1, 358, '/task_notification/notification', 'POST', 'JSON', '{\"title\": \"\", \"isRead\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"message\": \"\", \"createBy\": \"\", \"readTime\": \"\", \"updateBy\": \"\", \"extraData\": \"\", \"businessId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"businessType\": \"\", \"notificationId\": \"\", \"notificationType\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3654, 'Export Report Api Workflow Report List', '1', NULL, NULL, 1, 356, '/report/api_workflow_report/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3655, 'Get Websocket Debug Status', '1', NULL, NULL, 1, 357, '/ws/debug/status', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3652, 'Delete Report Api Workflow Report', '1', NULL, NULL, 1, 356, '/report/api_workflow_report/{report_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3653, 'Query Detail Report Api Workflow Report', '1', NULL, NULL, 1, 356, '/report/api_workflow_report/{report_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3648, 'Export Item Api Param Item List', '1', NULL, NULL, 1, 355, '/api_param_item/item/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3649, 'Get Report Api Workflow Report List', '1', NULL, NULL, 1, 356, '/report/api_workflow_report/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3650, 'Add Report Api Workflow Report', '1', NULL, NULL, 1, 356, '/report/api_workflow_report', 'POST', 'JSON', '{\"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"endTime\": \"\", \"createBy\": \"\", \"duration\": \"\", \"reportId\": \"\", \"updateBy\": \"\", \"isSuccess\": \"\", \"startTime\": \"\", \"createTime\": \"\", \"reportData\": \"\", \"totalCases\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"failedCases\": \"\", \"triggerType\": \"\", \"successCases\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3651, 'Edit Report Api Workflow Report', '1', NULL, NULL, 1, 356, '/report/api_workflow_report', 'PUT', 'JSON', '{\"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"endTime\": \"\", \"createBy\": \"\", \"duration\": \"\", \"reportId\": \"\", \"updateBy\": \"\", \"isSuccess\": \"\", \"startTime\": \"\", \"createTime\": \"\", \"reportData\": \"\", \"totalCases\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"failedCases\": \"\", \"triggerType\": \"\", \"successCases\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3646, 'Delete Item Api Param Item', '1', NULL, NULL, 1, 355, '/api_param_item/item/{key_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3647, 'Query Detail Item Api Param Item', '1', NULL, NULL, 1, 355, '/api_param_item/item/{key_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3643, 'Get Item Api Param Item List', '1', NULL, NULL, 1, 355, '/api_param_item/item/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3644, 'Add Item Api Param Item', '1', NULL, NULL, 1, 355, '/api_param_item/item', 'POST', 'JSON', '[{\"key\": \"\", \"item\": {}, \"keyId\": \"\", \"value\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"groupName\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"parameterizationId\": \"\"}]', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3645, 'Edit Item Api Param Item1', '1', NULL, NULL, 1, 355, '/api_param_item/item', 'PUT', 'JSON', '[{\"key\": \"\", \"item\": {}, \"keyId\": \"\", \"value\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"groupName\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"parameterizationId\": \"\"}]', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3640, 'Delete Table Api Param Table', '1', NULL, NULL, 1, 354, '/api_param_table/table/{parameterization_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3641, 'Query Detail Table Api Param Table', '1', NULL, NULL, 1, 354, '/api_param_table/table/{parameterization_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3642, 'Export Table Api Param Table List', '1', NULL, NULL, 1, 354, '/api_param_table/table/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3636, 'Delete Item Api Param Item', '1', NULL, NULL, 1, 354, '/api_param_table/table/row/{key_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3637, 'Get Table Api Param Table List', '1', NULL, NULL, 1, 354, '/api_param_table/table/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3638, 'Add Table Api Param Table', '1', NULL, NULL, 1, 354, '/api_param_table/table', 'POST', 'JSON', '{\"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"parameterizationId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3639, 'Edit Table Api Param Table', '1', NULL, NULL, 1, 354, '/api_param_table/table', 'PUT', 'JSON', '{\"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"parameterizationId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3635, 'Edit Item Api Paramitem', '1', NULL, NULL, 1, 354, '/api_param_table/table/row', 'PUT', 'JSON', '{\"key\": \"\", \"item\": {}, \"keyId\": \"\", \"value\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"groupName\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"parameterizationId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3634, 'Edit Item Api Paramitem', '1', NULL, NULL, 1, 354, '/api_param_table/table/row', 'POST', 'JSON', '{\"key\": \"\", \"item\": {}, \"keyId\": \"\", \"value\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"groupName\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"parameterizationId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3631, 'Delete Api Test Execution Log Execution Log', '1', NULL, NULL, 1, 353, '/api_test_execution_log/execution_log/{log_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3632, 'Query Detail Api Test Execution Log Execution Log', '1', NULL, NULL, 1, 353, '/api_test_execution_log/execution_log/{log_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3633, 'Export Api Test Execution Log Execution Log List', '1', NULL, NULL, 1, 353, '/api_test_execution_log/execution_log/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3630, 'Edit Api Test Execution Log Execution Log', '1', NULL, NULL, 1, 353, '/api_test_execution_log/execution_log', 'PUT', 'JSON', '{\"name\": \"\", \"path\": \"\", \"logId\": \"\", \"caseId\": \"\", \"method\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": 0, \"createBy\": \"\", \"reportId\": \"\", \"updateBy\": \"\", \"eventType\": \"\", \"isSuccess\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"responseTime\": \"\", \"executionData\": \"\", \"executionTime\": \"\", \"assertionSuccess\": \"\", \"responseStatusCode\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3628, 'Get Api Test Execution Log Execution Log List', '1', NULL, NULL, 1, 353, '/api_test_execution_log/execution_log/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3629, 'Add Api Test Execution Log Execution Log', '1', NULL, NULL, 1, 353, '/api_test_execution_log/execution_log', 'POST', 'JSON', '{\"name\": \"\", \"path\": \"\", \"logId\": \"\", \"caseId\": \"\", \"method\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": 0, \"createBy\": \"\", \"reportId\": \"\", \"updateBy\": \"\", \"eventType\": \"\", \"isSuccess\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"responseTime\": \"\", \"executionData\": \"\", \"executionTime\": \"\", \"assertionSuccess\": \"\", \"responseStatusCode\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3626, 'Query Detail Api Worknodes Worknodes', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes/{node_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3627, 'Export Api Worknodes Worknodes List', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3624, 'Copy Api Worknodes', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes/copy/{worknodeid}', 'POST', 'JSON', '{\"nodeId\": 0, \"targetParentId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3625, 'Delete Api Worknodes Worknodes', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes/{node_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3623, 'Edit Api Worknodes Sort', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes/sort', 'PUT', 'JSON', '[{\"name\": \"未命名\", \"type\": \"\", \"isRun\": \"\", \"config\": \"\", \"nodeId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"childrenIds\": \"\", \"description\": \"\"}]', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3622, 'Edit Api Worknodes Worknodes', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes', 'PUT', 'JSON', '{\"name\": \"未命名\", \"type\": \"\", \"isRun\": \"\", \"config\": \"\", \"nodeId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"childrenIds\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3618, 'Query Detail Api Worknode Executions Worknode Executions', '1', NULL, NULL, 1, 351, '/api_worknode_executions/worknode_executions/{node_execution_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3619, 'Export Api Worknode Executions Worknode Executions List', '1', NULL, NULL, 1, 351, '/api_worknode_executions/worknode_executions/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3620, 'Get Api Worknodes Worknodes List', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3621, 'Add Api Worknodes Worknodes', '1', NULL, NULL, 1, 352, '/api_worknodes/worknodes', 'POST', 'JSON', '{\"name\": \"未命名\", \"type\": \"\", \"isRun\": \"\", \"config\": \"\", \"nodeId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"caseIds\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"afterNodeId\": \"\", \"childrenIds\": \"\", \"curlCommand\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3617, 'Delete Api Worknode Executions Worknode Executions', '1', NULL, NULL, 1, 351, '/api_worknode_executions/worknode_executions/{node_execution_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3616, 'Edit Api Worknode Executions Worknode Executions', '1', NULL, NULL, 1, 351, '/api_worknode_executions/worknode_executions', 'PUT', 'JSON', '{\"nodeId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"status\": \"\", \"delFlag\": \"\", \"endTime\": \"\", \"createBy\": \"\", \"duration\": \"\", \"loopItem\": \"\", \"updateBy\": \"\", \"createdAt\": \"\", \"inputData\": \"\", \"loopIndex\": \"\", \"startTime\": \"\", \"createTime\": \"\", \"outputData\": \"\", \"retryCount\": \"\", \"updateTime\": \"\", \"description\": \"\", \"errorDetails\": \"\", \"errorMessage\": \"\", \"conditionResult\": \"\", \"contextSnapshot\": \"\", \"nodeExecutionId\": \"\", \"workflowExecutionId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3615, 'Add Api Worknode Executions Worknode Executions', '1', NULL, NULL, 1, 351, '/api_worknode_executions/worknode_executions', 'POST', 'JSON', '{\"nodeId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"status\": \"\", \"delFlag\": \"\", \"endTime\": \"\", \"createBy\": \"\", \"duration\": \"\", \"loopItem\": \"\", \"updateBy\": \"\", \"createdAt\": \"\", \"inputData\": \"\", \"loopIndex\": \"\", \"startTime\": \"\", \"createTime\": \"\", \"outputData\": \"\", \"retryCount\": \"\", \"updateTime\": \"\", \"description\": \"\", \"errorDetails\": \"\", \"errorMessage\": \"\", \"conditionResult\": \"\", \"contextSnapshot\": \"\", \"nodeExecutionId\": \"\", \"workflowExecutionId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3614, 'Get Api Worknode Executions Worknode Executions List', '1', NULL, NULL, 1, 351, '/api_worknode_executions/worknode_executions/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3612, 'Query Detail Api Workflow Executions Workflow Executions', '1', NULL, NULL, 1, 350, '/api_workflow_executions/workflow_executions/{workflow_execution_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3613, 'Export Api Workflow Executions Workflow Executions List', '1', NULL, NULL, 1, 350, '/api_workflow_executions/workflow_executions/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3611, 'Delete Api Workflow Executions Workflow Executions', '1', NULL, NULL, 1, 350, '/api_workflow_executions/workflow_executions/{workflow_execution_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3610, 'Edit Api Workflow Executions Workflow Executions', '1', NULL, NULL, 1, 350, '/api_workflow_executions/workflow_executions', 'PUT', 'JSON', '{\"remark\": \"\", \"sortNo\": \"\", \"status\": \"\", \"delFlag\": \"\", \"endTime\": \"\", \"createBy\": \"\", \"duration\": \"\", \"updateBy\": \"\", \"inputData\": \"\", \"startTime\": \"\", \"createTime\": \"\", \"outputData\": \"\", \"totalNodes\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"contextData\": \"\", \"description\": \"\", \"failedNodes\": \"\", \"errorDetails\": \"\", \"errorMessage\": \"\", \"skippedNodes\": \"\", \"successNodes\": \"\", \"workflowName\": \"\", \"workflowExecutionId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3608, 'Get Api Workflow Executions Workflow Executions List', '1', NULL, NULL, 1, 350, '/api_workflow_executions/workflow_executions/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3609, 'Add Api Workflow Executions Workflow Executions', '1', NULL, NULL, 1, 350, '/api_workflow_executions/workflow_executions', 'POST', 'JSON', '{\"remark\": \"\", \"sortNo\": \"\", \"status\": \"\", \"delFlag\": \"\", \"endTime\": \"\", \"createBy\": \"\", \"duration\": \"\", \"updateBy\": \"\", \"inputData\": \"\", \"startTime\": \"\", \"createTime\": \"\", \"outputData\": \"\", \"totalNodes\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"contextData\": \"\", \"description\": \"\", \"failedNodes\": \"\", \"errorDetails\": \"\", \"errorMessage\": \"\", \"skippedNodes\": \"\", \"successNodes\": \"\", \"workflowName\": \"\", \"workflowExecutionId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3607, 'Exec Workflow Stream', '1', NULL, NULL, 1, 349, '/workflow/workflow/exec', 'POST', 'JSON', '{\"name\": \"\", \"envId\": [null], \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"loopCount\": [1], \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": 0, \"description\": \"\", \"executionConfig\": {\"loopCount\": 1, \"threadingCount\": 1, \"parameterizationData\": []}, \"parentSubmoduleId\": \"\", \"parameterizationId\": [null]}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3606, 'Export Workflow Workflow List', '1', NULL, NULL, 1, 349, '/workflow/workflow/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3604, 'Delete Workflow Workflow', '1', NULL, NULL, 1, 349, '/workflow/workflow/{workflow_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3605, 'Query Detail Workflow Workflow', '1', NULL, NULL, 1, 349, '/workflow/workflow/{workflow_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3603, 'Edit Workflow Workflow', '1', NULL, NULL, 1, 349, '/workflow/workflow', 'PUT', 'JSON', '{\"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"executionConfig\": {\"loopCount\": 1, \"threadingCount\": 1, \"parameterizationData\": []}, \"parentSubmoduleId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3597, 'Query Detail Api Formdata Formdata', '1', NULL, NULL, 1, 348, '/api_formdata/formdata/{formdata_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3598, 'Export Api Formdata Formdata List', '1', NULL, NULL, 1, 348, '/api_formdata/formdata/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3599, 'Get Workflow Workflow List', '1', NULL, NULL, 1, 349, '/workflow/workflow/tree', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3600, 'Get Workflow Workflowtable List', '1', NULL, NULL, 1, 349, '/workflow/workflow/workflowtable', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3601, 'Get Workflow Workflow List', '1', NULL, NULL, 1, 349, '/workflow/workflow/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3602, 'Add Workflow Workflow', '1', NULL, NULL, 1, 349, '/workflow/workflow', 'POST', 'JSON', '{\"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"workflowId\": \"\", \"description\": \"\", \"executionConfig\": {\"loopCount\": 1, \"threadingCount\": 1, \"parameterizationData\": []}, \"parentSubmoduleId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3595, 'Edit Api Formdata Formdata', '1', NULL, NULL, 1, 348, '/api_formdata/formdata', 'PUT', 'JSON', '{\"key\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"updateBy\": \"\", \"createTime\": \"\", \"formdataId\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\", \"formFileConfig\": []}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3596, 'Delete Api Formdata Formdata', '1', NULL, NULL, 1, 348, '/api_formdata/formdata/{formdata_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3593, 'Get Api Formdata Formdata List', '1', NULL, NULL, 1, 348, '/api_formdata/formdata/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3594, 'Add Api Formdata Formdata', '1', NULL, NULL, 1, 348, '/api_formdata/formdata', 'POST', 'JSON', '{\"key\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"updateBy\": \"\", \"createTime\": \"\", \"formdataId\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\", \"formFileConfig\": []}', 1, 200, 0, '{}', '', '2025-12-31 14:49:57', '', '2025-12-31 14:49:57', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3591, 'Query Detail Api Teardown Teardown', '1', NULL, NULL, 1, 347, '/api_teardown/teardown/{teardown_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3592, 'Export Api Teardown Teardown List', '1', NULL, NULL, 1, 347, '/api_teardown/teardown/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3590, 'Delete Api Teardown Teardown', '1', NULL, NULL, 1, 347, '/api_teardown/teardown/{teardown_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3589, 'Edit Api Teardown Teardown', '1', NULL, NULL, 1, 347, '/api_teardown/teardown', 'PUT', 'JSON', '{\"name\": \"\", \"isRun\": \"\", \"caseId\": \"\", \"remark\": \"\", \"script\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"jsonpath\": \"\", \"updateBy\": \"\", \"waitTime\": \"\", \"createTime\": \"\", \"databaseId\": \"\", \"teardownId\": \"\", \"updateTime\": \"\", \"dbOperation\": \"\", \"description\": \"\", \"extractIndex\": \"\", \"teardownType\": \"\", \"variableName\": \"\", \"responseCookie\": \"\", \"responseHeader\": \"\", \"xpathExpression\": \"\", \"extractVariables\": [{}], \"extractIndexIsRun\": \"\", \"regularExpression\": \"\", \"extractVariableMethod\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3587, 'Get Api Teardown Teardown List', '1', NULL, NULL, 1, 347, '/api_teardown/teardown/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3588, 'Add Api Teardown Teardown', '1', NULL, NULL, 1, 347, '/api_teardown/teardown', 'POST', 'JSON', '{\"name\": \"\", \"isRun\": \"\", \"caseId\": \"\", \"remark\": \"\", \"script\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"jsonpath\": \"\", \"updateBy\": \"\", \"waitTime\": \"\", \"createTime\": \"\", \"databaseId\": \"\", \"teardownId\": \"\", \"updateTime\": \"\", \"dbOperation\": \"\", \"description\": \"\", \"extractIndex\": \"\", \"teardownType\": \"\", \"variableName\": \"\", \"responseCookie\": \"\", \"responseHeader\": \"\", \"xpathExpression\": \"\", \"extractVariables\": [{}], \"extractIndexIsRun\": \"\", \"regularExpression\": \"\", \"extractVariableMethod\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3584, 'Delete Api Setup Setup', '1', NULL, NULL, 1, 346, '/api_setup/setup/{setup_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3585, 'Query Detail Api Setup Setup', '1', NULL, NULL, 1, 346, '/api_setup/setup/{setup_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3586, 'Export Api Setup Setup List', '1', NULL, NULL, 1, 346, '/api_setup/setup/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3583, 'Edit Api Setup Setup', '1', NULL, NULL, 1, 346, '/api_setup/setup', 'PUT', 'JSON', '{\"name\": \"\", \"isRun\": \"\", \"caseId\": \"\", \"remark\": \"\", \"script\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"setupId\": \"\", \"createBy\": \"\", \"jsonpath\": \"\", \"updateBy\": \"\", \"waitTime\": \"\", \"setupType\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"extractIndex\": \"\", \"variableName\": \"\", \"dbConnectionId\": \"\", \"extractVariables\": [{}], \"extractIndexIsRun\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3581, 'Get Api Setup Setup List', '1', NULL, NULL, 1, 346, '/api_setup/setup/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3582, 'Add Api Setup Setup', '1', NULL, NULL, 1, 346, '/api_setup/setup', 'POST', 'JSON', '{\"name\": \"\", \"isRun\": \"\", \"caseId\": \"\", \"remark\": \"\", \"script\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"setupId\": \"\", \"createBy\": \"\", \"jsonpath\": \"\", \"updateBy\": \"\", \"waitTime\": \"\", \"setupType\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"extractIndex\": \"\", \"variableName\": \"\", \"dbConnectionId\": \"\", \"extractVariables\": [{}], \"extractIndexIsRun\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3578, 'Delete Api Params Params', '1', NULL, NULL, 1, 345, '/api_params/params/{param_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3579, 'Query Detail Api Params Params', '1', NULL, NULL, 1, 345, '/api_params/params/{param_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3580, 'Export Api Params Params List', '1', NULL, NULL, 1, 345, '/api_params/params/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3574, 'Export Api Headers Headers List', '1', NULL, NULL, 1, 344, '/api_headers/headers/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3575, 'Get Api Params Params List', '1', NULL, NULL, 1, 345, '/api_params/params/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3576, 'Add Api Params Params', '1', NULL, NULL, 1, 345, '/api_params/params', 'POST', 'JSON', '{\"key\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"paramId\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"updateBy\": \"\", \"createTime\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3577, 'Edit Api Params Params', '1', NULL, NULL, 1, 345, '/api_params/params', 'PUT', 'JSON', '{\"key\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"paramId\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"updateBy\": \"\", \"createTime\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3571, 'Edit Api Headers Headers', '1', NULL, NULL, 1, 344, '/api_headers/headers', 'PUT', 'JSON', '{\"key\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"headerId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3572, 'Delete Api Headers Headers', '1', NULL, NULL, 1, 344, '/api_headers/headers/{header_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3573, 'Query Detail Api Headers Headers', '1', NULL, NULL, 1, 344, '/api_headers/headers/{header_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3570, 'Add Api Headers Headers', '1', NULL, NULL, 1, 344, '/api_headers/headers', 'POST', 'JSON', '{\"key\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"headerId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3569, 'Get Api Headers Headers List', '1', NULL, NULL, 1, 344, '/api_headers/headers/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3568, 'Export Api Cookies Cookies List', '1', NULL, NULL, 1, 343, '/api_cookies/cookies/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3566, 'Delete Api Cookies Cookies', '1', NULL, NULL, 1, 343, '/api_cookies/cookies/{cookie_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3567, 'Query Detail Api Cookies Cookies', '1', NULL, NULL, 1, 343, '/api_cookies/cookies/{cookie_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3565, 'Edit Api Cookies Cookies', '1', NULL, NULL, 1, 343, '/api_cookies/cookies', 'PUT', 'JSON', '{\"key\": \"\", \"path\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"domain\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"cookieId\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"updateBy\": \"\", \"createTime\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3564, 'Add Api Cookies Cookies', '1', NULL, NULL, 1, 343, '/api_cookies/cookies', 'POST', 'JSON', '{\"key\": \"\", \"path\": \"\", \"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"domain\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"cookieId\": \"\", \"createBy\": \"\", \"dataType\": \"string\", \"updateBy\": \"\", \"createTime\": \"\", \"isRequired\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3563, 'Get Api Cookies Cookies List', '1', NULL, NULL, 1, 343, '/api_cookies/cookies/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3560, 'Delete Api Assertions Assertions', '1', NULL, NULL, 1, 342, '/api_assertions/assertions/{assertion_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3561, 'Query Detail Api Assertions Assertions', '1', NULL, NULL, 1, 342, '/api_assertions/assertions/{assertion_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3562, 'Export Api Assertions Assertions List', '1', NULL, NULL, 1, 342, '/api_assertions/assertions/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3559, 'Edit Api Assertions Assertions', '1', NULL, NULL, 1, 342, '/api_assertions/assertions', 'PUT', 'JSON', '{\"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"jsonpath\": \"\", \"updateBy\": \"\", \"assertType\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"assertionId\": \"\", \"description\": \"\", \"jsonpathIndex\": \"\", \"assertionMethod\": \"\", \"extractIndexIsRun\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3555, '导入HAR文件接口', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/har/import', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3556, '从cURL命令导入接口', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/curl/import', 'POST', 'JSON', '{\"projectId\": 0, \"curlCommand\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3557, 'Get Api Assertions Assertions List', '1', NULL, NULL, 1, 342, '/api_assertions/assertions/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3558, 'Add Api Assertions Assertions', '1', NULL, NULL, 1, 342, '/api_assertions/assertions', 'POST', 'JSON', '{\"isRun\": \"\", \"value\": \"\", \"caseId\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"jsonpath\": \"\", \"updateBy\": \"\", \"assertType\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"assertionId\": \"\", \"description\": \"\", \"jsonpathIndex\": \"\", \"assertionMethod\": \"\", \"extractIndexIsRun\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3550, '从URL预览OpenAPI/Swagger接口', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/openapi/preview/url', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3551, '从文件预览OpenAPI/Swagger接口', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/openapi/preview/file', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3552, '从URL导入OpenAPI/Swagger接口', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/openapi/import/url', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3553, '从文件导入OpenAPI/Swagger接口', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/openapi/import/file', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3554, '预览HAR文件接口', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/har/preview', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3549, 'Export Api Test Cases Test Cases List', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3548, 'Copy To Case', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/copy_to_case', 'POST', 'JSON', '{\"name\": \"\", \"path\": \"\", \"isRun\": \"\", \"sleep\": \"\", \"caseId\": \"\", \"copyId\": \"\", \"method\": \"GET\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"caseType\": \"\", \"createBy\": \"\", \"jsonData\": {}, \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"statusCode\": \"\", \"updateTime\": \"\", \"description\": \"\", \"requestType\": \"NONE\", \"parentCaseId\": \"\", \"caseFileConfig\": \"\", \"responseExample\": \"\", \"parentSubmoduleId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3547, 'Copy Api Test Cases Test Cases', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/copy', 'POST', 'JSON', '{\"name\": \"\", \"path\": \"\", \"isRun\": \"\", \"sleep\": \"\", \"caseId\": \"\", \"copyId\": \"\", \"method\": \"GET\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"caseType\": \"\", \"createBy\": \"\", \"jsonData\": {}, \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"statusCode\": \"\", \"updateTime\": \"\", \"description\": \"\", \"requestType\": \"NONE\", \"parentCaseId\": \"\", \"caseFileConfig\": \"\", \"responseExample\": \"\", \"parentSubmoduleId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3546, 'Query Detail Api Test Cases Test Cases', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/{case_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3545, 'Delete Api Test Cases Test Cases', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/{case_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3544, 'Exec Api Test Cases', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/exec', 'POST', 'JSON', '{\"name\": \"\", \"path\": \"\", \"envId\": 1, \"isRun\": \"\", \"sleep\": \"\", \"caseId\": \"\", \"copyId\": \"\", \"method\": \"GET\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"caseType\": \"\", \"createBy\": \"\", \"jsonData\": {}, \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"statusCode\": \"\", \"updateTime\": \"\", \"description\": \"\", \"requestType\": \"NONE\", \"parentCaseId\": \"\", \"caseFileConfig\": \"\", \"responseExample\": \"\", \"parentSubmoduleId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3543, 'Edit Api Test Cases Test Cases', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/sort', 'POST', 'JSON', '[{\"name\": \"\", \"path\": \"\", \"isRun\": \"\", \"sleep\": \"\", \"caseId\": \"\", \"copyId\": \"\", \"method\": \"GET\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"caseType\": \"\", \"createBy\": \"\", \"jsonData\": {}, \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"statusCode\": \"\", \"updateTime\": \"\", \"description\": \"\", \"requestType\": \"NONE\", \"parentCaseId\": \"\", \"caseFileConfig\": \"\", \"responseExample\": \"\", \"parentSubmoduleId\": \"\"}]', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3542, 'Edit Api Test Cases Test Cases', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases', 'PUT', 'JSON', '{\"name\": \"\", \"path\": \"\", \"isRun\": \"\", \"sleep\": \"\", \"caseId\": \"\", \"copyId\": \"\", \"method\": \"GET\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"caseType\": \"\", \"createBy\": \"\", \"formdata\": [], \"jsonData\": {}, \"updateBy\": \"\", \"projectId\": \"\", \"setupList\": [], \"createTime\": \"\", \"paramsList\": [], \"statusCode\": \"\", \"updateTime\": \"\", \"cookiesList\": [], \"description\": \"\", \"headersList\": [], \"requestType\": \"NONE\", \"parentCaseId\": \"\", \"teardownList\": [], \"assertionList\": [], \"caseFileConfig\": \"\", \"responseExample\": \"\", \"parentSubmoduleId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3541, 'Edit Api Test Cases Test Cases', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases', 'POST', 'JSON', '{\"name\": \"\", \"path\": \"\", \"user\": \"\", \"isRun\": \"\", \"sleep\": \"\", \"caseId\": \"\", \"copyId\": \"\", \"inputs\": \"\", \"method\": \"GET\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"caseType\": \"\", \"createBy\": \"\", \"jsonData\": {}, \"updateBy\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"statusCode\": \"\", \"updateTime\": \"\", \"description\": \"\", \"requestType\": \"NONE\", \"parentCaseId\": \"\", \"responseMode\": \"streaming\", \"caseFileConfig\": \"\", \"responseExample\": \"\", \"parentSubmoduleId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3538, 'Export Api Cache Data Cache Data List', '1', NULL, NULL, 1, 340, '/api_cache_data/cache_data/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3539, 'Upload Files', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/importbyfile/{type}', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3540, 'Get Api Test Cases Test Cases List', '1', NULL, NULL, 1, 341, '/api_test_cases/test_cases/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3536, 'Delete Api Cache Data Cache Data', '1', NULL, NULL, 1, 340, '/api_cache_data/cache_data/{ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3537, 'Query Detail Api Cache Data Cache Data', '1', NULL, NULL, 1, 340, '/api_cache_data/cache_data/{id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3535, 'Edit Api Cache Data Cache Data', '1', NULL, NULL, 1, 340, '/api_cache_data/cache_data', 'PUT', 'JSON', '{\"id\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"cacheKey\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"cacheValue\": \"\", \"createTime\": \"\", \"sourceType\": \"\", \"updateTime\": \"\", \"description\": \"\", \"environmentId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3532, 'Export Api Services Services List', '1', NULL, NULL, 1, 339, '/api_services/services/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3533, 'Get Api Cache Data Cache Data List', '1', NULL, NULL, 1, 340, '/api_cache_data/cache_data/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3534, 'Add Api Cache Data Cache Data', '1', NULL, NULL, 1, 340, '/api_cache_data/cache_data', 'POST', 'JSON', '{\"id\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"cacheKey\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"cacheValue\": \"\", \"createTime\": \"\", \"sourceType\": \"\", \"updateTime\": \"\", \"description\": \"\", \"environmentId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:56', '', '2025-12-31 14:49:56', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3530, 'Delete Api Services Services', '1', NULL, NULL, 1, 339, '/api_services/services/{ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3531, 'Query Detail Api Services Services', '1', NULL, NULL, 1, 339, '/api_services/services/{id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3529, 'Edit Api Services Services', '1', NULL, NULL, 1, 339, '/api_services/services', 'PUT', 'JSON', '{\"id\": \"\", \"url\": \"\", \"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"isDefault\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"environmentId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3526, 'Export Api Project Submodules Project Submodules List', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3527, 'Get Api Services Services List', '1', NULL, NULL, 1, 339, '/api_services/services/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3528, 'Add Api Services Services', '1', NULL, NULL, 1, 339, '/api_services/services', 'POST', 'JSON', '{\"id\": \"\", \"url\": \"\", \"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"isDefault\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"environmentId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3522, 'Get Api Project Submodules Workflow Tree', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/workflow_tree', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3523, 'Edit Api Project Submodules Project Submodules Sort', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/sort', 'PUT', 'JSON', '[{\"id\": \"\", \"name\": \"\", \"type\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"ancestors\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\"}]', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3524, 'Delete Api Project Submodules Project Submodules', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/{ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3525, 'Query Detail Api Project Submodules Project Submodules', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/{id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3521, 'Edit Api Project Submodules Project Submodules', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules', 'PUT', 'JSON', '{\"id\": \"\", \"name\": \"\", \"type\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"ancestors\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3520, 'Add Api Project Submodules Project Submodules', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules', 'POST', 'JSON', '{\"id\": \"\", \"name\": \"\", \"type\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"ancestors\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3519, 'Get Api Project Submodules Project Submodules List', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3518, 'Get Api Project Submodules Api Tree', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/api_tree', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3517, 'Get Api Project Submodules Project Submodules Tree', '1', NULL, NULL, 1, 338, '/api_project_submodules/project_submodules/tree', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3516, 'Export Api Environments Environments List', '1', NULL, NULL, 1, 337, '/api_environments/environments/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3515, 'Query Detail Api Environments Environments', '1', NULL, NULL, 1, 337, '/api_environments/environments/{id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3514, 'Delete Api Environments Environments', '1', NULL, NULL, 1, 337, '/api_environments/environments/{ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3513, 'Get Api Environments Config', '1', NULL, NULL, 1, 337, '/api_environments/environments/config', 'PUT', 'JSON', '{\"id\": \"\", \"url\": \"\", \"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"cacheList\": [], \"isDefault\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"globalHeaders\": [], \"requestTimeout\": 5000}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3512, 'Add Api Environments Environments', '1', NULL, NULL, 1, 337, '/api_environments/environments/config', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3511, 'Edit Api Environments Environments', '1', NULL, NULL, 1, 337, '/api_environments/environments', 'PUT', 'JSON', '{\"id\": \"\", \"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"isDefault\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"globalHeaders\": [{\"key\": \"Content-Type\", \"value\": \"application/json\", \"is_run\": true, \"description\": \"内容类型\"}], \"requestTimeout\": 5000}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3506, 'Export Api Databases Api Databases List', '1', NULL, NULL, 1, 336, '/api_databases/api_databases/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3507, 'Test Api Databases Connection', '1', NULL, NULL, 1, 336, '/api_databases/api_databases/test/{id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3508, 'Execute Api Databases Script', '1', NULL, NULL, 1, 336, '/api_databases/api_databases/execute', 'POST', 'JSON', '{\"dbId\": 0, \"script\": \"\", \"projectId\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3509, 'Get Api Environments Environments List', '1', NULL, NULL, 1, 337, '/api_environments/environments/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3510, 'Add Api Environments Environments', '1', NULL, NULL, 1, 337, '/api_environments/environments', 'POST', 'JSON', '{\"id\": \"\", \"name\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"isDefault\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\", \"globalHeaders\": [{\"key\": \"Content-Type\", \"value\": \"application/json\", \"is_run\": true, \"description\": \"内容类型\"}], \"requestTimeout\": 5000}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3504, 'Delete Api Databases Api Databases', '1', NULL, NULL, 1, 336, '/api_databases/api_databases/{ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3505, 'Query Detail Api Databases Api Databases', '1', NULL, NULL, 1, 336, '/api_databases/api_databases/{id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3503, 'Edit Api Databases Api Databases', '1', NULL, NULL, 1, 336, '/api_databases/api_databases', 'PUT', 'JSON', '{\"id\": \"\", \"host\": \"\", \"name\": \"\", \"port\": \"\", \"dbType\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"password\": \"\", \"updateBy\": \"\", \"username\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3501, 'Get Api Databases Api Databases List', '1', NULL, NULL, 1, 336, '/api_databases/api_databases/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3502, 'Add Api Databases Api Databases', '1', NULL, NULL, 1, 336, '/api_databases/api_databases', 'POST', 'JSON', '{\"id\": \"\", \"host\": \"\", \"name\": \"\", \"port\": \"\", \"dbType\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"password\": \"\", \"updateBy\": \"\", \"username\": \"\", \"projectId\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3498, 'Delete Api Project Project', '1', NULL, NULL, 1, 335, '/api_project/project/{ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3499, 'Query Detail Api Project Project', '1', NULL, NULL, 1, 335, '/api_project/project/{id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3500, 'Export Api Project Project List', '1', NULL, NULL, 1, 335, '/api_project/project/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3496, 'Add Api Project Project', '1', NULL, NULL, 1, 335, '/api_project/project', 'POST', 'JSON', '{\"id\": \"\", \"name\": \"\", \"type\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"ancestors\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3497, 'Edit Api Project Project', '1', NULL, NULL, 1, 335, '/api_project/project', 'PUT', 'JSON', '{\"id\": \"\", \"name\": \"\", \"type\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"ancestors\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"description\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3495, 'Get Api Project Project List', '1', NULL, NULL, 1, 335, '/api_project/project/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3491, 'Gen Code Local', '1', NULL, NULL, 1, 334, '/tool/gen/genCode/{table_name}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3494, 'Sync Db', '1', NULL, NULL, 1, 334, '/tool/gen/synchDb/{table_name}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3493, 'Preview Code', '1', NULL, NULL, 1, 334, '/tool/gen/preview/{table_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3492, 'Query Detail Gen Table', '1', NULL, NULL, 1, 334, '/tool/gen/{table_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3488, 'Delete Gen Table', '1', NULL, NULL, 1, 334, '/tool/gen/{table_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3489, 'Create Table', '1', NULL, NULL, 1, 334, '/tool/gen/createTable', 'POST', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3490, 'Batch Gen Code', '1', NULL, NULL, 1, 334, '/tool/gen/batchGenCode', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3487, 'Edit Gen Table', '1', NULL, NULL, 1, 334, '/tool/gen', 'PUT', 'JSON', '{\"sub\": \"\", \"crud\": \"\", \"tree\": \"\", \"params\": \"\", \"remark\": \"\", \"columns\": \"\", \"genPath\": \"\", \"genType\": \"\", \"options\": \"\", \"tableId\": \"\", \"createBy\": \"\", \"pkColumn\": \"\", \"subTable\": \"\", \"treeCode\": \"\", \"treeName\": \"\", \"updateBy\": \"\", \"className\": \"\", \"tableName\": \"\", \"createTime\": \"\", \"moduleName\": \"\", \"tplWebType\": \"\", \"updateTime\": \"\", \"packageName\": \"\", \"tplCategory\": \"\", \"businessName\": \"\", \"functionName\": \"\", \"parentMenuId\": \"\", \"subTableName\": \"\", \"tableComment\": \"\", \"functionAuthor\": \"\", \"parentMenuName\": \"\", \"subTableFkName\": \"\", \"treeParentCode\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3485, 'Get Gen Db Table List', '1', NULL, NULL, 1, 334, '/tool/gen/db/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3486, 'Import Gen Table', '1', NULL, NULL, 1, 334, '/tool/gen/importTable', 'POST', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3484, 'Get Gen Table List', '1', NULL, NULL, 1, 334, '/tool/gen/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3482, 'Common Download', '1', NULL, NULL, 1, 333, '/common/download', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3483, 'Common Download Resource', '1', NULL, NULL, 1, 333, '/common/download/resource', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3478, 'Clear Monitor Cache Name', '1', NULL, NULL, 1, 332, '/monitor/cache/clearCacheName/{cache_name}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3479, 'Clear Monitor Cache Key', '1', NULL, NULL, 1, 332, '/monitor/cache/clearCacheKey/{cache_key}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3480, 'Clear Monitor Cache All', '1', NULL, NULL, 1, 332, '/monitor/cache/clearCacheAll', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3481, 'Common Upload', '1', NULL, NULL, 1, 333, '/common/upload', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3476, 'Get Monitor Cache Key', '1', NULL, NULL, 1, 332, '/monitor/cache/getKeys/{cache_name}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3477, 'Get Monitor Cache Value', '1', NULL, NULL, 1, 332, '/monitor/cache/getValue/{cache_name}/{cache_key}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3475, 'Get Monitor Cache Name', '1', NULL, NULL, 1, 332, '/monitor/cache/getNames', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3473, 'Get Monitor Server Info', '1', NULL, NULL, 1, 331, '/monitor/server', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3474, 'Get Monitor Cache Info', '1', NULL, NULL, 1, 332, '/monitor/cache', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3470, 'Clear System Job Log', '1', NULL, NULL, 1, 330, '/monitor/jobLog/clean', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3471, 'Delete System Job Log', '1', NULL, NULL, 1, 330, '/monitor/jobLog/{job_log_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3472, 'Export System Job Log List', '1', NULL, NULL, 1, 330, '/monitor/jobLog/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3468, 'Export System Job List', '1', NULL, NULL, 1, 330, '/monitor/job/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3469, 'Get System Job Log List', '1', NULL, NULL, 1, 330, '/monitor/jobLog/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3467, 'Query Detail System Job', '1', NULL, NULL, 1, 330, '/monitor/job/{job_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3466, 'Delete System Job', '1', NULL, NULL, 1, 330, '/monitor/job/{job_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3465, 'Execute System Job', '1', NULL, NULL, 1, 330, '/monitor/job/run', 'PUT', 'JSON', '{\"jobId\": \"\", \"remark\": \"\", \"status\": \"\", \"jobArgs\": \"\", \"jobName\": \"\", \"createBy\": \"\", \"jobGroup\": \"\", \"updateBy\": \"\", \"jobKwargs\": \"\", \"concurrent\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"jobExecutor\": \"\", \"invokeTarget\": \"\", \"misfirePolicy\": \"\", \"cronExpression\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3464, 'Change System Job Status', '1', NULL, NULL, 1, 330, '/monitor/job/changeStatus', 'PUT', 'JSON', '{\"type\": \"\", \"jobId\": \"\", \"remark\": \"\", \"status\": \"\", \"jobArgs\": \"\", \"jobName\": \"\", \"createBy\": \"\", \"jobGroup\": \"\", \"updateBy\": \"\", \"jobKwargs\": \"\", \"concurrent\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"jobExecutor\": \"\", \"invokeTarget\": \"\", \"misfirePolicy\": \"\", \"cronExpression\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3463, 'Edit System Job', '1', NULL, NULL, 1, 330, '/monitor/job', 'PUT', 'JSON', '{\"type\": \"\", \"jobId\": \"\", \"remark\": \"\", \"status\": \"\", \"jobArgs\": \"\", \"jobName\": \"\", \"createBy\": \"\", \"jobGroup\": \"\", \"updateBy\": \"\", \"jobKwargs\": \"\", \"concurrent\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"jobExecutor\": \"\", \"invokeTarget\": \"\", \"misfirePolicy\": \"\", \"cronExpression\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3462, 'Add System Job', '1', NULL, NULL, 1, 330, '/monitor/job', 'POST', 'JSON', '{\"jobId\": \"\", \"remark\": \"\", \"status\": \"\", \"jobArgs\": \"\", \"jobName\": \"\", \"createBy\": \"\", \"jobGroup\": \"\", \"updateBy\": \"\", \"jobKwargs\": \"\", \"concurrent\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"jobExecutor\": \"\", \"invokeTarget\": \"\", \"misfirePolicy\": \"\", \"cronExpression\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3461, 'Get System Job List', '1', NULL, NULL, 1, 330, '/monitor/job/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3457, 'Query Detail System File', '1', NULL, NULL, 1, 328, '/system/file/{file_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3458, 'Export System File List', '1', NULL, NULL, 1, 328, '/system/file/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3459, 'Get Monitor Online List', '1', NULL, NULL, 1, 329, '/monitor/online/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3460, 'Delete Monitor Online', '1', NULL, NULL, 1, 329, '/monitor/online/{token_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:55', '', '2025-12-31 14:49:55', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3455, 'Edit System File', '1', NULL, NULL, 1, 328, '/system/file', 'PUT', 'JSON', '{\"bizTag\": \"\", \"fileId\": \"\", \"isTemp\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"fileExt\": \"\", \"fileUrl\": \"\", \"createBy\": \"\", \"fileHash\": \"\", \"filePath\": \"\", \"fileSize\": \"\", \"mimeType\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"storedName\": \"\", \"updateTime\": \"\", \"description\": \"\", \"storageType\": \"\", \"originalName\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3456, 'Delete System File', '1', NULL, NULL, 1, 328, '/system/file/{file_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3454, 'Add System File', '1', NULL, NULL, 1, 328, '/system/file', 'POST', 'JSON', '{\"bizTag\": \"\", \"fileId\": \"\", \"isTemp\": \"\", \"remark\": \"\", \"sortNo\": \"\", \"delFlag\": \"\", \"fileExt\": \"\", \"fileUrl\": \"\", \"createBy\": \"\", \"fileHash\": \"\", \"filePath\": \"\", \"fileSize\": \"\", \"mimeType\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"storedName\": \"\", \"updateTime\": \"\", \"description\": \"\", \"storageType\": \"\", \"originalName\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3451, 'Upload Single File', '1', NULL, NULL, 1, 328, '/system/file/upload/single', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3452, 'Serve File', '1', NULL, NULL, 1, 328, '/system/file/CaseGo/upload_path/files/{file_path}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3453, 'Get System File List', '1', NULL, NULL, 1, 328, '/system/file/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3450, 'Upload Files', '1', NULL, NULL, 1, 328, '/system/file/upload', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3448, 'Unlock System User', '1', NULL, NULL, 1, 327, '/monitor/logininfor/unlock/{user_name}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3449, 'Export System Login Log List', '1', NULL, NULL, 1, 327, '/monitor/logininfor/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3447, 'Delete System Login Log', '1', NULL, NULL, 1, 327, '/monitor/logininfor/{info_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3446, 'Clear System Login Log', '1', NULL, NULL, 1, 327, '/monitor/logininfor/clean', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3442, 'Clear System Operation Log', '1', NULL, NULL, 1, 327, '/monitor/operlog/clean', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3443, 'Delete System Operation Log', '1', NULL, NULL, 1, 327, '/monitor/operlog/{oper_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3444, 'Export System Operation Log List', '1', NULL, NULL, 1, 327, '/monitor/operlog/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3445, 'Get System Login Log List', '1', NULL, NULL, 1, 327, '/monitor/logininfor/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3439, 'Delete System Notice', '1', NULL, NULL, 1, 326, '/system/notice/{notice_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3440, 'Query Detail System Post', '1', NULL, NULL, 1, 326, '/system/notice/{notice_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3441, 'Get System Operation Log List', '1', NULL, NULL, 1, 327, '/monitor/operlog/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3437, 'Add System Notice', '1', NULL, NULL, 1, 326, '/system/notice', 'POST', 'JSON', '{\"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"noticeId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"noticeType\": \"\", \"updateTime\": \"\", \"noticeTitle\": \"\", \"noticeContent\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3438, 'Edit System Notice', '1', NULL, NULL, 1, 326, '/system/notice', 'PUT', 'JSON', '{\"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"noticeId\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"noticeType\": \"\", \"updateTime\": \"\", \"noticeTitle\": \"\", \"noticeContent\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3433, 'Query Detail System Config', '1', NULL, NULL, 1, 325, '/system/config/{config_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3434, 'Query System Config', '1', NULL, NULL, 1, 325, '/system/config/configKey/{config_key}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3435, 'Export System Config List', '1', NULL, NULL, 1, 325, '/system/config/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3436, 'Get System Notice List', '1', NULL, NULL, 1, 326, '/system/notice/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3430, 'Edit System Config', '1', NULL, NULL, 1, 325, '/system/config', 'PUT', 'JSON', '{\"remark\": \"\", \"configId\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"configKey\": \"\", \"configName\": \"\", \"configType\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"configValue\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3432, 'Delete System Config', '1', NULL, NULL, 1, 325, '/system/config/{config_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3431, 'Refresh System Config', '1', NULL, NULL, 1, 325, '/system/config/refreshCache', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3429, 'Add System Config', '1', NULL, NULL, 1, 325, '/system/config', 'POST', 'JSON', '{\"remark\": \"\", \"configId\": \"\", \"createBy\": \"\", \"updateBy\": \"\", \"configKey\": \"\", \"configName\": \"\", \"configType\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"configValue\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3428, 'Get System Config List', '1', NULL, NULL, 1, 325, '/system/config/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3427, 'Export System Dict Data List', '1', NULL, NULL, 1, 324, '/system/dict/data/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3425, 'Delete System Dict Data', '1', NULL, NULL, 1, 324, '/system/dict/data/{dict_codes}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3426, 'Query Detail System Dict Data', '1', NULL, NULL, 1, 324, '/system/dict/data/{dict_code}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3424, 'Edit System Dict Data', '1', NULL, NULL, 1, 324, '/system/dict/data', 'PUT', 'JSON', '{\"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"cssClass\": \"\", \"dictCode\": \"\", \"dictSort\": \"\", \"dictType\": \"\", \"updateBy\": \"\", \"dictLabel\": \"\", \"dictValue\": \"\", \"isDefault\": \"\", \"listClass\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3423, 'Add System Dict Data', '1', NULL, NULL, 1, 324, '/system/dict/data', 'POST', 'JSON', '{\"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"cssClass\": \"\", \"dictCode\": \"\", \"dictSort\": \"\", \"dictType\": \"\", \"updateBy\": \"\", \"dictLabel\": \"\", \"dictValue\": \"\", \"isDefault\": \"\", \"listClass\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3422, 'Get System Dict Data List', '1', NULL, NULL, 1, 324, '/system/dict/data/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3420, 'Export System Dict Type List', '1', NULL, NULL, 1, 324, '/system/dict/type/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3421, 'Query System Dict Type Data', '1', NULL, NULL, 1, 324, '/system/dict/data/type/{dict_type}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3417, 'Delete System Dict Type', '1', NULL, NULL, 1, 324, '/system/dict/type/{dict_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3418, 'Query System Dict Type Options', '1', NULL, NULL, 1, 324, '/system/dict/type/optionselect', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3419, 'Query Detail System Dict Type', '1', NULL, NULL, 1, 324, '/system/dict/type/{dict_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3415, 'Edit System Dict Type', '1', NULL, NULL, 1, 324, '/system/dict/type', 'PUT', 'JSON', '{\"dictId\": \"\", \"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"dictName\": \"\", \"dictType\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3416, 'Refresh System Dict', '1', NULL, NULL, 1, 324, '/system/dict/type/refreshCache', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3413, 'Get System Dict Type List', '1', NULL, NULL, 1, 324, '/system/dict/type/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3414, 'Add System Dict Type', '1', NULL, NULL, 1, 324, '/system/dict/type', 'POST', 'JSON', '{\"dictId\": \"\", \"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"dictName\": \"\", \"dictType\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3412, 'Export System Post List', '1', NULL, NULL, 1, 323, '/system/post/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3411, 'Query Detail System Post', '1', NULL, NULL, 1, 323, '/system/post/{post_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3410, 'Delete System Post', '1', NULL, NULL, 1, 323, '/system/post/{post_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3409, 'Edit System Post', '1', NULL, NULL, 1, 323, '/system/post', 'PUT', 'JSON', '{\"postId\": \"\", \"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"postCode\": \"\", \"postName\": \"\", \"postSort\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3408, 'Add System Post', '1', NULL, NULL, 1, 323, '/system/post', 'POST', 'JSON', '{\"postId\": \"\", \"remark\": \"\", \"status\": \"\", \"createBy\": \"\", \"postCode\": \"\", \"postName\": \"\", \"postSort\": \"\", \"updateBy\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3407, 'Get System Post List', '1', NULL, NULL, 1, 323, '/system/post/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3406, 'Query Detail System Dept', '1', NULL, NULL, 1, 322, '/system/dept/{dept_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3405, 'Delete System Dept', '1', NULL, NULL, 1, 322, '/system/dept/{dept_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3404, 'Edit System Dept', '1', NULL, NULL, 1, 322, '/system/dept', 'PUT', 'JSON', '{\"email\": \"\", \"phone\": \"\", \"deptId\": \"\", \"leader\": \"\", \"status\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"deptName\": \"\", \"orderNum\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"ancestors\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3403, 'Add System Dept', '1', NULL, NULL, 1, 322, '/system/dept', 'POST', 'JSON', '{\"email\": \"\", \"phone\": \"\", \"deptId\": \"\", \"leader\": \"\", \"status\": \"\", \"delFlag\": \"\", \"createBy\": \"\", \"deptName\": \"\", \"orderNum\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"ancestors\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3399, 'Delete System Menu', '1', NULL, NULL, 1, 321, '/system/menu/{menu_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3400, 'Query Detail System Menu', '1', NULL, NULL, 1, 321, '/system/menu/{menu_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3401, 'Get System Dept Tree For Edit Option', '1', NULL, NULL, 1, 322, '/system/dept/list/exclude/{dept_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3402, 'Get System Dept List', '1', NULL, NULL, 1, 322, '/system/dept/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3398, 'Edit System Menu', '1', NULL, NULL, 1, 321, '/system/menu', 'PUT', 'JSON', '{\"icon\": \"\", \"path\": \"\", \"perms\": \"\", \"query\": \"\", \"menuId\": \"\", \"remark\": \"\", \"status\": \"\", \"isCache\": \"\", \"isFrame\": \"\", \"visible\": \"\", \"createBy\": \"\", \"menuName\": \"\", \"menuType\": \"\", \"orderNum\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"component\": \"\", \"routeName\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3395, 'Get System Role Menu Tree', '1', NULL, NULL, 1, 321, '/system/menu/roleMenuTreeselect/{role_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3396, 'Get System Menu List', '1', NULL, NULL, 1, 321, '/system/menu/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3397, 'Add System Menu', '1', NULL, NULL, 1, 321, '/system/menu', 'POST', 'JSON', '{\"icon\": \"\", \"path\": \"\", \"perms\": \"\", \"query\": \"\", \"menuId\": \"\", \"remark\": \"\", \"status\": \"\", \"isCache\": \"\", \"isFrame\": \"\", \"visible\": \"\", \"createBy\": \"\", \"menuName\": \"\", \"menuType\": \"\", \"orderNum\": \"\", \"parentId\": \"\", \"updateBy\": \"\", \"component\": \"\", \"routeName\": \"\", \"createTime\": \"\", \"updateTime\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3391, 'Add System Role User', '1', NULL, NULL, 1, 320, '/system/role/authUser/selectAll', 'PUT', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3392, 'Cancel System Role User', '1', NULL, NULL, 1, 320, '/system/role/authUser/cancel', 'PUT', 'JSON', '{\"roleId\": \"\", \"userId\": \"\", \"roleIds\": \"\", \"userIds\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3393, 'Batch Cancel System Role User', '1', NULL, NULL, 1, 320, '/system/role/authUser/cancelAll', 'PUT', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3394, 'Get System Menu Tree', '1', NULL, NULL, 1, 321, '/system/menu/treeselect', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3390, 'Get System Unallocated User List', '1', NULL, NULL, 1, 320, '/system/role/authUser/unallocatedList', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3386, 'Query Detail System Role', '1', NULL, NULL, 1, 320, '/system/role/{role_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3387, 'Export System Role List', '1', NULL, NULL, 1, 320, '/system/role/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3389, 'Get System Allocated User List', '1', NULL, NULL, 1, 320, '/system/role/authUser/allocatedList', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3388, 'Reset System Role Status', '1', NULL, NULL, 1, 320, '/system/role/changeStatus', 'PUT', 'JSON', '{\"type\": \"\", \"admin\": false, \"remark\": \"\", \"roleId\": \"\", \"status\": \"\", \"delFlag\": \"\", \"deptIds\": [], \"menuIds\": [], \"roleKey\": \"\", \"createBy\": \"\", \"roleName\": \"\", \"roleSort\": \"\", \"updateBy\": \"\", \"dataScope\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"deptCheckStrictly\": \"\", \"menuCheckStrictly\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3385, 'Delete System Role', '1', NULL, NULL, 1, 320, '/system/role/{role_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3384, 'Edit System Role Datascope', '1', NULL, NULL, 1, 320, '/system/role/dataScope', 'PUT', 'JSON', '{\"type\": \"\", \"admin\": false, \"remark\": \"\", \"roleId\": \"\", \"status\": \"\", \"delFlag\": \"\", \"deptIds\": [], \"menuIds\": [], \"roleKey\": \"\", \"createBy\": \"\", \"roleName\": \"\", \"roleSort\": \"\", \"updateBy\": \"\", \"dataScope\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"deptCheckStrictly\": \"\", \"menuCheckStrictly\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3383, 'Edit System Role', '1', NULL, NULL, 1, 320, '/system/role', 'PUT', 'JSON', '{\"type\": \"\", \"admin\": false, \"remark\": \"\", \"roleId\": \"\", \"status\": \"\", \"delFlag\": \"\", \"deptIds\": [], \"menuIds\": [], \"roleKey\": \"\", \"createBy\": \"\", \"roleName\": \"\", \"roleSort\": \"\", \"updateBy\": \"\", \"dataScope\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"deptCheckStrictly\": \"\", \"menuCheckStrictly\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3379, 'Update System Role User', '1', NULL, NULL, 1, 319, '/system/user/authRole', 'PUT', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3380, 'Get System Role Dept Tree', '1', NULL, NULL, 1, 320, '/system/role/deptTree/{role_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3381, 'Get System Role List', '1', NULL, NULL, 1, 320, '/system/role/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3382, 'Add System Role', '1', NULL, NULL, 1, 320, '/system/role', 'POST', 'JSON', '{\"type\": \"\", \"admin\": false, \"remark\": \"\", \"roleId\": \"\", \"status\": \"\", \"delFlag\": \"\", \"deptIds\": [], \"menuIds\": [], \"roleKey\": \"\", \"createBy\": \"\", \"roleName\": \"\", \"roleSort\": \"\", \"updateBy\": \"\", \"dataScope\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"deptCheckStrictly\": \"\", \"menuCheckStrictly\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3376, 'Export System User Template', '1', NULL, NULL, 1, 319, '/system/user/importTemplate', 'POST', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3377, 'Export System User List', '1', NULL, NULL, 1, 319, '/system/user/export', 'POST', 'x_www_form_urlencoded', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3378, 'Get System Allocated Role List', '1', NULL, NULL, 1, 319, '/system/user/authRole/{user_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:54', '', '2025-12-31 14:49:54', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3375, 'Batch Import System User', '1', NULL, NULL, 1, 319, '/system/user/importData', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3374, 'Reset System User Password', '1', NULL, NULL, 1, 319, '/system/user/profile/updatePwd', 'PUT', 'JSON', '{\"newPassword\": \"\", \"oldPassword\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3373, 'Change System User Profile Avatar', '1', NULL, NULL, 1, 319, '/system/user/profile/avatar', 'POST', 'Form_Data', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3371, 'Query Detail System User', '1', NULL, NULL, 1, 319, '/system/user/', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3372, 'Query Detail System User', '1', NULL, NULL, 1, 319, '/system/user/{user_id}', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3369, 'Query Detail System User Profile', '1', NULL, NULL, 1, 319, '/system/user/profile', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3370, 'Change System User Profile Info', '1', NULL, NULL, 1, 319, '/system/user/profile', 'PUT', 'JSON', '{\"sex\": \"\", \"dept\": \"\", \"role\": [], \"admin\": false, \"email\": \"\", \"avatar\": \"\", \"deptId\": \"\", \"remark\": \"\", \"status\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"loginIp\": \"\", \"postIds\": \"\", \"roleIds\": \"\", \"createBy\": \"\", \"nickName\": \"\", \"password\": \"\", \"updateBy\": \"\", \"userName\": \"\", \"userType\": \"\", \"loginDate\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"phonenumber\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3368, 'Change System User Status', '1', NULL, NULL, 1, 319, '/system/user/changeStatus', 'PUT', 'JSON', '{\"sex\": \"\", \"role\": [], \"type\": \"\", \"admin\": false, \"email\": \"\", \"avatar\": \"\", \"deptId\": \"\", \"remark\": \"\", \"status\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"loginIp\": \"\", \"postIds\": [], \"roleIds\": [], \"createBy\": \"\", \"nickName\": \"\", \"password\": \"\", \"updateBy\": \"\", \"userName\": \"\", \"userType\": \"\", \"loginDate\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"phonenumber\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3367, 'Reset System User Pwd', '1', NULL, NULL, 1, 319, '/system/user/resetPwd', 'PUT', 'JSON', '{\"sex\": \"\", \"role\": [], \"type\": \"\", \"admin\": false, \"email\": \"\", \"avatar\": \"\", \"deptId\": \"\", \"remark\": \"\", \"status\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"loginIp\": \"\", \"postIds\": [], \"roleIds\": [], \"createBy\": \"\", \"nickName\": \"\", \"password\": \"\", \"updateBy\": \"\", \"userName\": \"\", \"userType\": \"\", \"loginDate\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"phonenumber\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3366, 'Delete System User', '1', NULL, NULL, 1, 319, '/system/user/{user_ids}', 'DELETE', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3365, 'Edit System User', '1', NULL, NULL, 1, 319, '/system/user', 'PUT', 'JSON', '{\"sex\": \"\", \"role\": [], \"type\": \"\", \"admin\": false, \"email\": \"\", \"avatar\": \"\", \"deptId\": \"\", \"remark\": \"\", \"status\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"loginIp\": \"\", \"postIds\": [], \"roleIds\": [], \"createBy\": \"\", \"nickName\": \"\", \"password\": \"\", \"updateBy\": \"\", \"userName\": \"\", \"userType\": \"\", \"loginDate\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"phonenumber\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3364, 'Add System User', '1', NULL, NULL, 1, 319, '/system/user', 'POST', 'JSON', '{\"sex\": \"\", \"type\": \"\", \"admin\": false, \"email\": \"\", \"avatar\": \"\", \"deptId\": \"\", \"remark\": \"\", \"status\": \"\", \"userId\": \"\", \"delFlag\": \"\", \"loginIp\": \"\", \"postIds\": [], \"roleIds\": [], \"createBy\": \"\", \"nickName\": \"\", \"password\": \"\", \"updateBy\": \"\", \"userName\": \"\", \"userType\": \"\", \"loginDate\": \"\", \"createTime\": \"\", \"updateTime\": \"\", \"phonenumber\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3362, 'Get System Dept Tree', '1', NULL, NULL, 1, 319, '/system/user/deptTree', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3363, 'Get System User List', '1', NULL, NULL, 1, 319, '/system/user/list', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3361, 'Get Captcha Image', '1', NULL, NULL, 1, 318, '/captchaImage', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', '', '2025-12-31 14:49:53', NULL, NULL, 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3360, 'Logout', '1', NULL, NULL, 1, 317, '/logout', 'POST', 'NONE', '\"\"', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:45', NULL, '', 3, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3359, 'Register User', '1', NULL, NULL, 1, 317, '/register', 'POST', 'JSON', '{\"code\": \"\", \"uuid\": \"\", \"password\": \"\", \"username\": \"\", \"confirmPassword\": \"\"}', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:45', NULL, NULL, 4, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3358, 'Get Login User Routers', '1', NULL, NULL, 1, 317, '/getRouters', 'GET', 'NONE', 'null', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:45', NULL, NULL, 5, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3356, 'Login', '1', NULL, NULL, 1, 317, '/login', 'POST', 'x_www_form_urlencoded', '\"\"', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:52:45', NULL, '', 1, 0, NULL);
INSERT INTO `api_test_cases` VALUES (3357, 'Get Login User Info', '1', NULL, NULL, 1, 317, '/getInfo', 'GET', 'NONE', '\"\"', 1, 200, 0, '{}', '', '2025-12-31 14:49:53', 'admin', '2025-12-31 14:53:05', NULL, '', 2, 0, NULL);

-- ----------------------------
-- Table structure for api_test_execution_log
-- ----------------------------
DROP TABLE IF EXISTS `api_test_execution_log`;
CREATE TABLE `api_test_execution_log`  (
  `log_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '执行日志ID',
  `case_id` int(11) NULL DEFAULT NULL COMMENT '测试用例ID',
  `execution_time` datetime NOT NULL COMMENT '执行时间',
  `is_success` tinyint(1) NULL DEFAULT NULL COMMENT '是否执行成功',
  `execution_data` json NULL COMMENT '完整执行数据',
  `response_status_code` int(11) NULL DEFAULT NULL COMMENT '响应状态码',
  `response_time` float NULL DEFAULT NULL COMMENT '响应时间(秒)',
  `assertion_success` tinyint(1) NULL DEFAULT NULL COMMENT '断言是否成功',
  `method` enum('POST','GET','PUT','DELETE','OPTIONS','HEAD','PATCH','TRACE','CONNECT','COPY','LINK','UNLINK','PURGE','LOCK','UNLOCK','MKCOL','MOVE','PROPFIND','REPORT','VIEW') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求方法',
  `path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求路径',
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '测试用例名称',
  `workflow_id` bigint(20) NULL DEFAULT NULL COMMENT 'workflow_id',
  `report_id` bigint(20) NULL DEFAULT NULL COMMENT 'report_id',
  `event_type` enum('HEARTBEAT','WORKFLOW_START','WORKFLOW_END','NODE_START','NODE_END','NODE_ERROR','LOOP_START','LOOP_ITERATION','LOOP_END','PROGRESS','LOG','ERROR','CONFIG_INFO','CASE_RESULT') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '类型',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`log_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 38962 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '接口测试执行日志表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_test_execution_log
-- ----------------------------

-- ----------------------------
-- Table structure for api_workflow
-- ----------------------------
DROP TABLE IF EXISTS `api_workflow`;
CREATE TABLE `api_workflow`  (
  `workflow_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '执行器名称',
  `execution_config` json NULL COMMENT '执行配置',
  `parent_submodule_id` bigint(20) NULL DEFAULT NULL COMMENT '父级模块ID',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  `project_id` bigint(20) NULL DEFAULT NULL COMMENT '父级模块ID',
  PRIMARY KEY (`workflow_id`) USING BTREE,
  INDEX `ix_workflow_name`(`name`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 39 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '测试执行器主表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_workflow
-- ----------------------------
INSERT INTO `api_workflow` VALUES (1, '测试套件1', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 137, 'david', '2025-08-28 15:42:19', 'admin', '2025-08-28 21:17:00', '123', '123', 123, 0, 1);
INSERT INTO `api_workflow` VALUES (2, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 137, 'david', '2025-08-28 15:42:25', 'admin', '2025-08-28 21:17:03', '123', '123', 123, 1, 1);
INSERT INTO `api_workflow` VALUES (3, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 137, 'admin', '2025-08-28 21:17:09', 'admin', '2025-08-28 21:17:09', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (4, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 137, 'admin', '2025-08-28 21:17:18', 'admin', '2025-08-28 21:17:18', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (5, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 138, 'david', '2025-08-28 21:18:34', 'david', '2025-08-28 21:18:34', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (6, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 138, 'david', '2025-08-28 21:18:44', 'david', '2025-08-28 21:18:44', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (7, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 1, 'david', '2025-08-29 00:14:59', 'david', '2025-08-29 00:14:59', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (8, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 1, 'david', '2025-08-30 21:41:03', 'david', '2025-08-30 21:41:03', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (9, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', 1, 'david', '2025-08-31 00:59:07', 'david', '2025-08-31 00:59:07', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (10, '1', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', NULL, 'admin', '2025-10-24 14:17:14', 'admin', '2025-10-24 14:17:14', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (11, '1', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', NULL, 'admin', '2025-10-24 14:17:28', 'admin', '2025-10-24 14:17:28', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (12, '123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', NULL, 'admin', '2025-10-31 11:01:02', 'admin', '2025-10-31 11:01:02', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (13, '123123', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', NULL, 'admin', '2025-10-31 11:01:07', 'admin', '2025-10-31 11:01:07', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (14, '111', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', NULL, 'admin', '2025-11-03 21:53:32', 'admin', '2025-11-03 21:53:32', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (15, '11', '{\"env_id\": 1, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": 1, \"parameterization_data\": []}', NULL, 'admin', '2025-11-12 00:07:38', 'admin', '2025-11-12 00:07:38', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (16, '123', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', NULL, 'admin', '2025-11-15 10:03:41', 'admin', '2025-11-15 10:03:41', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (32, '4444444444444444444444', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', NULL, 'admin', '2025-12-08 15:43:16', 'admin', '2025-12-08 15:43:16', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (31, '4444444', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', 218, 'admin', '2025-12-08 15:43:11', 'admin', '2025-12-08 15:43:11', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (30, '1111111111111111', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', 214, 'admin', '2025-12-08 15:39:52', 'admin', '2025-12-08 15:54:15', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (29, '66666666666', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', 214, 'admin', '2025-12-08 11:53:00', 'admin', '2025-12-08 11:53:00', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (28, '55555', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', 214, 'admin', '2025-12-08 11:52:54', 'admin', '2025-12-08 11:52:54', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (27, '333333', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', 214, 'admin', '2025-12-08 11:52:46', 'admin', '2025-12-08 11:52:46', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (26, '333333333', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', 214, 'admin', '2025-12-08 11:52:38', 'admin', '2025-12-08 11:52:38', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (33, '111', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', NULL, 'admin', '2025-12-09 13:46:21', 'admin', '2025-12-09 13:46:21', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (34, '自动化1', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', NULL, 'admin', '2025-12-09 14:09:44', 'admin', '2025-12-09 14:09:44', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (35, '1', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', NULL, 'admin', '2025-12-15 23:01:30', 'admin', '2025-12-15 23:01:30', NULL, NULL, 1, 0, 46);
INSERT INTO `api_workflow` VALUES (36, '888', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', 138, 'admin', '2025-12-16 15:23:57', 'admin', '2025-12-16 15:23:57', NULL, NULL, 1, 0, 1);
INSERT INTO `api_workflow` VALUES (37, '示例注册-登录流程', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', NULL, 'admin', '2025-12-18 14:51:06', 'admin', '2025-12-18 14:51:06', NULL, NULL, 1, 1, 1);
INSERT INTO `api_workflow` VALUES (38, '111', '{\"env_id\": null, \"loop_count\": 1, \"threading_count\": 1, \"parameterization_id\": null, \"parameterization_data\": []}', NULL, 'admin', '2025-12-26 17:33:13', 'admin', '2025-12-26 17:33:13', NULL, NULL, 1, 1, 1);

-- ----------------------------
-- Table structure for api_workflow_executions
-- ----------------------------
DROP TABLE IF EXISTS `api_workflow_executions`;
CREATE TABLE `api_workflow_executions`  (
  `workflow_execution_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `workflow_id` bigint(20) NULL DEFAULT NULL COMMENT '执行器ID',
  `workflow_name` bigint(20) NULL DEFAULT NULL COMMENT '执行名称',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执行状态',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
  `duration` int(11) NULL DEFAULT NULL COMMENT '执行时长(秒)',
  `input_data` json NULL COMMENT '输入数据',
  `output_data` json NULL COMMENT '输出数据',
  `context_data` json NULL COMMENT '上下文数据',
  `total_nodes` int(11) NULL DEFAULT NULL COMMENT '总节点数',
  `success_nodes` int(11) NULL DEFAULT NULL COMMENT '成功节点数',
  `failed_nodes` int(11) NULL DEFAULT NULL COMMENT '失败节点数',
  `skipped_nodes` int(11) NULL DEFAULT NULL COMMENT '跳过节点数',
  `error_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '错误信息',
  `error_details` json NULL COMMENT '错误详情',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`workflow_execution_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '执行器执行记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_workflow_executions
-- ----------------------------

-- ----------------------------
-- Table structure for api_workflow_report
-- ----------------------------
DROP TABLE IF EXISTS `api_workflow_report`;
CREATE TABLE `api_workflow_report`  (
  `report_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '报告ID',
  `workflow_id` bigint(20) NOT NULL COMMENT '执行器ID',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '报告名称',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
  `total_cases` int(11) NULL DEFAULT NULL COMMENT '总用例数',
  `success_cases` int(11) NULL DEFAULT NULL COMMENT '成功用例数',
  `failed_cases` int(11) NULL DEFAULT NULL COMMENT '失败用例数',
  `duration` float NULL DEFAULT NULL COMMENT '总耗时(秒)',
  `is_success` tinyint(1) NULL DEFAULT NULL COMMENT '是否全部成功',
  `report_data` json NULL COMMENT '完整报告JSON数据',
  `trigger_type` enum('manual','cron','api','system') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '触发类型',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`report_id`) USING BTREE,
  INDEX `ix_report_workflow_id`(`workflow_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 4372 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '自动化测试执行报告表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_workflow_report
-- ----------------------------

-- ----------------------------
-- Table structure for api_workflow_schemas
-- ----------------------------
DROP TABLE IF EXISTS `api_workflow_schemas`;
CREATE TABLE `api_workflow_schemas`  (
  `schemas_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `schema_version` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'Schema版本',
  `node_types` json NOT NULL COMMENT '节点类型定义',
  `condition_operators` json NOT NULL COMMENT '条件操作符列表',
  `error_handling_options` json NOT NULL COMMENT '错误处理选项',
  `custom_config` json NULL COMMENT '自定义配置',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`schemas_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '执行器schema配置表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_workflow_schemas
-- ----------------------------

-- ----------------------------
-- Table structure for api_worknode_executions
-- ----------------------------
DROP TABLE IF EXISTS `api_worknode_executions`;
CREATE TABLE `api_worknode_executions`  (
  `node_execution_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `workflow_execution_id` bigint(20) NOT NULL COMMENT '执行器执行记录ID',
  `node_id` bigint(20) NOT NULL COMMENT '节点ID',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '执行状态',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束时间',
  `duration` int(11) NULL DEFAULT NULL COMMENT '执行时长(毫秒)',
  `input_data` json NULL COMMENT '输入数据',
  `output_data` json NULL COMMENT '输出数据',
  `context_snapshot` json NULL COMMENT '执行时上下文快照',
  `loop_index` int(11) NULL DEFAULT NULL COMMENT '循环索引',
  `loop_item` json NULL COMMENT '循环项数据',
  `condition_result` tinyint(1) NULL DEFAULT NULL COMMENT '条件判断结果',
  `error_message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '错误信息',
  `error_details` json NULL COMMENT '错误详情',
  `retry_count` int(11) NULL DEFAULT NULL COMMENT '重试次数',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`node_execution_id`) USING BTREE,
  INDEX `ix_node_execution_id`(`node_execution_id`) USING BTREE,
  INDEX `ix_node_executions_node_id`(`node_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '节点执行记录表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_worknode_executions
-- ----------------------------

-- ----------------------------
-- Table structure for api_worknodes
-- ----------------------------
DROP TABLE IF EXISTS `api_worknodes`;
CREATE TABLE `api_worknodes`  (
  `node_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `workflow_id` bigint(20) NULL DEFAULT NULL COMMENT '所属执行器ID',
  `parent_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '父节点ID',
  `name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '节点名称',
  `type` enum('IF','ELSE','FOR','FOREACH','GROUP','TASK') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '节点类型',
  `is_run` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用执行',
  `children_ids` json NULL COMMENT '子结点列表',
  `config` json NULL COMMENT '节点配置信息',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`node_id`) USING BTREE,
  INDEX `ix_executor_nodes_parent_id`(`parent_id`) USING BTREE,
  INDEX `ix_executor_nodes_type`(`type`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 752 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '执行器节点表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of api_worknodes
-- ----------------------------

-- ----------------------------
-- Table structure for apscheduler_jobs
-- ----------------------------
DROP TABLE IF EXISTS `apscheduler_jobs`;
CREATE TABLE `apscheduler_jobs`  (
  `id` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务ID',
  `next_run_time` float NULL DEFAULT NULL COMMENT '下次运行时间',
  `job_state` blob NOT NULL COMMENT '任务状态数据',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_apscheduler_jobs_next_run_time`(`next_run_time` ASC) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of apscheduler_jobs
-- ----------------------------

-- ----------------------------
-- Table structure for gen_table
-- ----------------------------
DROP TABLE IF EXISTS `gen_table`;
CREATE TABLE `gen_table`  (
  `table_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '表名称',
  `table_comment` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '表描述',
  `sub_table_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关联子表的表名',
  `sub_table_fk_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '子表关联的外键名',
  `class_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '实体类名称',
  `tpl_category` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '使用的模板（crud单表操作 tree树表操作）',
  `tpl_web_type` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '前端模板类型（element-ui模版 element-plus模版）',
  `package_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '生成包路径',
  `module_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '生成模块名',
  `business_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '生成业务名',
  `function_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '生成功能名',
  `function_author` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '生成功能作者',
  `gen_type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '生成代码方式（0zip压缩包 1自定义路径）',
  `gen_path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '生成路径（不填默认项目路径）',
  `options` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '其它生成选项',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`table_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 43 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gen_table
-- ----------------------------
INSERT INTO `gen_table` VALUES (1, 'students', '很好的学生', NULL, NULL, 'Students', 'crud', 'element-plus', 'module_admin.system', 'system', 'students', '很好的学生', 'insistence', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-07-02 17:50:29', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table` VALUES (9, 'api_environments', '环境配置表', NULL, NULL, 'ApiEnvironments', 'crud', 'element-plus', 'module_admin.api_environments', 'api_environments', 'environments', '环境配置', 'insistence', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1061}', 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table` VALUES (12, 'api_databases', '数据库配置表', NULL, NULL, 'ApiDatabases', 'crud', 'element-plus', 'module_admin.system', 'system', 'databases', '数据库配置', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table` VALUES (13, 'api_services', '环境服务地址表', NULL, NULL, 'ApiServices', 'crud', 'element-plus', 'module_admin.api_services', 'api_services', 'services', '环境服务地址', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1061}', 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table` VALUES (15, 'api_project', '项目表', NULL, NULL, 'ApiProject', 'crud', 'element-plus', 'module_admin.api_project', 'api_project', 'project', '项目', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table` VALUES (16, 'api_project_submodules', '项目模块表', NULL, NULL, 'ApiProjectSubmodules', 'crud', 'element-plus', 'module_admin.api_project_submodules', 'api_project_submodules', 'project_submodules', '项目模块', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1061}', 'admin', '2025-08-01 09:29:30', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table` VALUES (18, 'api_cache_data', '环境缓存表', NULL, NULL, 'ApiCacheData', 'crud', 'element-plus', 'module_admin.api_cache_data', 'api_cache_data', 'cache_data', '环境缓存', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1061}', 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table` VALUES (22, 'api_assertions', '接口断言', NULL, NULL, 'ApiAssertions', 'crud', 'element-plus', 'module_admin.api_assertions', 'api_assertions', 'assertions', '接口断言', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (23, 'api_cookies', '接口请求Cookie', NULL, NULL, 'ApiCookies', 'crud', 'element-plus', 'module_admin.api_cookies', 'api_cookies', 'cookies', '接口请求Cookie', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (24, 'api_headers', '接口请求头', NULL, NULL, 'ApiHeaders', 'crud', 'element-plus', 'module_admin.api_headers', 'api_headers', 'headers', '接口请求头', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (25, 'api_params', '接口请求参数', NULL, NULL, 'ApiParams', 'crud', 'element-plus', 'module_admin.api_params', 'api_params', 'params', '接口请求参数', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (26, 'api_setup', '接口前置操作', NULL, NULL, 'ApiSetup', 'crud', 'element-plus', 'module_admin.api_setup', 'api_setup', 'setup', '接口前置操作', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (27, 'api_teardown', '接口后置操作', NULL, NULL, 'ApiTeardown', 'crud', 'element-plus', 'module_admin.api_teardown', 'api_teardown', 'teardown', '接口后置操作', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (28, 'api_test_cases', '接口用例表', NULL, NULL, 'ApiTestCases', 'crud', 'element-plus', 'module_admin.api_test_cases', 'api_test_cases', 'test_cases', '接口用例', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (30, 'api_formdata', '接口表单body', NULL, NULL, 'ApiFormdata', 'crud', 'element-plus', 'module_admin.api_formdata', 'api_formdata', 'formdata', '接口单body', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (31, 'sys_file', '附件表', NULL, NULL, 'SysFile', 'crud', 'element-plus', 'module_admin.system', 'system', 'file', '附件管理', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1}', 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (32, 'api_workflow', '测试执行器主表', NULL, NULL, 'ApiWorkflow', 'crud', 'element-plus', 'module_admin.api_workflow.workflow', 'workflow', 'workflow', '测试执行器主', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1157}', 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (33, 'api_workflow_executions', '执行器执行记录表', NULL, NULL, 'ApiWorkflowExecutions', 'crud', 'element-plus', 'module_admin.api_workflow.api_workflow_executions', 'api_workflow_executions', 'workflow_executions', '执行器执行记录', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (34, 'api_workflow_schemas', '执行器schema配置表', NULL, NULL, 'ApiWorkflowSchemas', 'crud', '', 'module_admin.system', 'system', 'schemas', '执行器schema配置', 'david', '0', '/', NULL, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (35, 'api_worknode_executions', '节点执行记录表', NULL, NULL, 'ApiWorknodeExecutions', 'crud', 'element-plus', 'module_admin.api_workflow.api_worknode_executions', 'api_worknode_executions', 'worknode_executions', '节点执行记录', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (36, 'api_worknodes', '执行器节点表', NULL, NULL, 'ApiWorknodes', 'crud', 'element-plus', 'module_admin.api_workflow.api_worknodes', 'api_worknodes', 'worknodes', '执行器节点', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (37, 'api_test_execution_log', '接口测试执行日志表', NULL, NULL, 'ApiTestExecutionLog', 'crud', 'element-plus', 'module_admin.api_testing.api_test_execution_log', 'api_test_execution_log', 'execution_log', '接口测试执行日志', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (38, 'api_param_item', '参数化数据表行', NULL, NULL, 'ApiParamItem', 'crud', 'element-plus', 'module_admin.api_workflow.api_param_item', 'item', 'api_param_item', '参数化数据行', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (39, 'api_param_table', '参数化数据表主表', NULL, NULL, 'ApiParamTable', 'crud', 'element-plus', 'module_admin.api_workflow.api_param_table', 'table', 'api_param_table', '参数化数据主', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": null}', 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (40, 'api_workflow_report', '自动化测试执行报告表', NULL, NULL, 'ApiWorkflowReport', 'crud', 'element-plus', 'module_admin.api_workflow.api_workflow_report', 'report', 'api_workflow_report', '自动化测试执行报告', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (41, 'api_notification', '通知消息表', NULL, NULL, 'ApiNotification', 'crud', 'element-plus', 'module_admin.system.notification', 'task_notification', 'notification', '通知消息', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table` VALUES (42, 'api_script_library', '公共脚本库', NULL, NULL, 'ApiScriptLibrary', 'crud', 'element-plus', 'module_admin.api_testing.api_script_library', 'api_script_library', 'script_library', '公共脚本库', 'david', '0', '/', '{\"treeCode\": null, \"treeParentCode\": null, \"treeName\": null, \"parentMenuId\": 1114}', 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for gen_table_column
-- ----------------------------
DROP TABLE IF EXISTS `gen_table_column`;
CREATE TABLE `gen_table_column`  (
  `column_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '编号',
  `table_id` bigint(20) NULL DEFAULT NULL COMMENT '归属表编号',
  `column_name` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '列名称',
  `column_comment` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '列描述',
  `column_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '列类型',
  `python_type` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'PYTHON类型',
  `python_field` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'PYTHON字段名',
  `is_pk` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否主键（1是）',
  `is_increment` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否自增（1是）',
  `is_required` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否必填（1是）',
  `is_unique` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否唯一（1是）',
  `is_insert` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否为插入字段（1是）',
  `is_edit` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否编辑字段（1是）',
  `is_list` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否列表字段（1是）',
  `is_query` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否查询字段（1是）',
  `query_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '查询方式（等于、不等于、大于、小于、范围）',
  `html_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）',
  `dict_type` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字典类型',
  `sort` int(11) NULL DEFAULT NULL COMMENT '排序',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`column_id`) USING BTREE,
  INDEX `table_id`(`table_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 701 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of gen_table_column
-- ----------------------------
INSERT INTO `gen_table_column` VALUES (1, 1, 'student_id', '学号（主键）', 'int(11)', 'int', 'studentId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', NULL, 1, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (2, 1, 'id_card', '身份证号', 'varchar(18)', 'str', 'idCard', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 2, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (3, 1, 'full_name', '姓名', 'varchar(50)', 'str', 'fullName', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', NULL, 3, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (4, 1, 'gender', '性别', 'enum(\'1\',\'2\',\'3\')', 'str', 'gender', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'radio', 'sys_user_sex', 4, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (5, 1, 'birth_date', '出生日期', 'date', 'date', 'birthDate', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', NULL, 5, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (6, 1, 'mobile', '手机号码', 'varchar(15)', 'str', 'mobile', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 6, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (7, 1, 'email', '电子邮箱', 'varchar(100)', 'str', 'email', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 7, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (8, 1, 'emergency_contact', '紧急联系人', 'varchar(50)', 'str', 'emergencyContact', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 8, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (9, 1, 'emergency_phone', '紧急联系电话', 'varchar(15)', 'str', 'emergencyPhone', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 9, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (10, 1, 'home_address', '家庭住址', 'varchar(200)', 'str', 'homeAddress', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 10, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (11, 1, 'enrollment_date', '入学日期', 'date', 'date', 'enrollmentDate', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', NULL, 11, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (12, 1, 'graduation_date', '预计毕业日期', 'date', 'date', 'graduationDate', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', NULL, 12, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (13, 1, 'major', '专业名称', 'varchar(50)', 'str', 'major', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 13, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (14, 1, 'class_name', '班级名称', 'varchar(20)', 'str', 'className', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', NULL, 14, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (15, 1, 'student_status', '学籍状态', 'enum(\'在读\',\'休学\',\'退学\',\'毕业\')', 'str', 'studentStatus', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'radio', NULL, 15, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (16, 1, 'gpa', '平均学分绩点', 'float', 'float', 'gpa', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 16, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (17, 1, 'english_level', '英语等级', 'enum(\'CET-4\',\'CET-6\',\'TEM-8\',\'无\')', 'str', 'englishLevel', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, NULL, 17, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (18, 1, 'scholarship', '是否获得奖学金', 'tinyint(1)', 'int', 'scholarship', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 18, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (19, 1, 'political_status', '政治面貌', 'enum(\'群众\',\'共青团员\',\'中共党员\')', 'str', 'politicalStatus', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'radio', NULL, 19, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (20, 1, 'dormitory', '宿舍号', 'varchar(20)', 'str', 'dormitory', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 20, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (21, 1, 'profile_photo', '照片路径', 'varchar(255)', 'str', 'profilePhoto', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 21, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, NULL);
INSERT INTO `gen_table_column` VALUES (23, 1, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 22, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (24, 1, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 23, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (25, 1, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 24, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (26, 1, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 25, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (27, 1, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 26, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (28, 1, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 27, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (29, 1, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 28, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (30, 1, 'del_flag', '删除标志 0正常 1删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 29, 'admin', '2025-07-03 09:52:51', 'admin', '2025-07-03 09:53:56', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (128, 9, 'id', '环境ID', 'int(11)', 'int', 'id', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (129, 9, 'name', '环境名称', 'varchar(100)', 'str', 'name', '0', '0', '1', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (130, 9, 'project_id', '所属项目ID', 'int(11)', 'int', 'projectId', '0', '0', '0', NULL, '1', '1', '0', '1', 'EQ', 'input', '', 3, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (131, 9, 'is_default', '是否为默认环境', 'tinyint(1)', 'int', 'isDefault', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'radio', 'user_is_defalut', 4, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (132, 9, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 5, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (133, 9, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '0', NULL, NULL, '1', 'EQ', 'datetime', '', 6, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (134, 9, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'input', '', 7, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (135, 9, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'datetime', '', 8, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (136, 9, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 9, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (137, 9, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 10, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (138, 9, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 11, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (139, 9, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 12, 'admin', '2025-07-30 17:26:26', 'admin', '2025-07-30 23:28:25', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (169, 12, 'id', '数据库ID', 'int(11)', 'int', 'id', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (170, 12, 'name', '数据库名称', 'varchar(100)', 'str', 'name', '0', '0', '1', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (171, 12, 'db_type', '数据库类型（如1 MySQL、2Redis，）', 'varchar(50)', 'str', 'dbType', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'select', '', 3, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (172, 12, 'host', '数据库主机', 'varchar(100)', 'str', 'host', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (173, 12, 'port', '数据库端口', 'int(11)', 'int', 'port', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (174, 12, 'username', '数据库用户名', 'varchar(100)', 'str', 'username', '0', '0', '1', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 6, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (175, 12, 'password', '数据库密码', 'varchar(100)', 'str', 'password', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (176, 12, 'project_id', '所属项目ID', 'int(11)', 'int', 'projectId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (177, 12, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 9, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (178, 12, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 10, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (179, 12, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 11, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (180, 12, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 12, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (181, 12, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 13, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (182, 12, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (183, 12, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 15, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (184, 12, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 16, 'admin', '2025-07-30 21:28:52', 'admin', '2025-07-30 21:39:52', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (185, 13, 'id', '服务ID', 'int(11)', 'int', 'id', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (186, 13, 'name', '服务名称', 'varchar(100)', 'str', 'name', '0', '0', '1', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (187, 13, 'url', '服务地址', 'varchar(200)', 'str', 'url', '0', '0', '1', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 3, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (188, 13, 'environment_id', '所属环境ID', 'int(11)', 'int', 'environmentId', '0', '0', '1', NULL, '0', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (189, 13, 'is_default', '是否为默认服务', 'tinyint(1)', 'int', 'isDefault', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'select', 'user_is_defalut', 5, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (190, 13, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 6, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (191, 13, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'datetime', '', 7, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (192, 13, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'input', '', 8, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (193, 13, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'datetime', '', 9, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (194, 13, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '0', '0', '0', NULL, 'EQ', 'input', '', 10, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (195, 13, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 11, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (196, 13, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 12, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (197, 13, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-07-30 22:57:24', 'admin', '2025-08-01 15:33:19', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (212, 15, 'id', 'ID', 'bigint(20)', 'int', 'id', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (213, 15, 'name', '项目名称', 'varchar(100)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (214, 15, 'type', '项目类型', 'enum(\'0\',\'1\',\'2\',\'3\')', 'str', 'type', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 3, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (215, 15, 'parent_id', '父部门id', 'bigint(20)', 'int', 'parentId', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 4, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (216, 15, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 5, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (217, 15, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '0', NULL, '1', NULL, 'EQ', 'datetime', '', 6, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (218, 15, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'input', '', 7, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (219, 15, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'datetime', '', 8, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (220, 15, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '0', '0', '0', NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (221, 15, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '0', '1', '0', 'EQ', 'input', '', 10, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (222, 15, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 11, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (223, 15, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 12, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (224, 15, 'ancestors', '祖级列表', 'varchar(50)', 'str', 'ancestors', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 13, 'admin', '2025-08-01 09:12:35', 'admin', '2025-08-01 09:14:43', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (225, 16, 'id', 'ID', 'bigint(20)', 'int', 'id', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', NULL, 1, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (226, 16, 'name', '模块名称', 'varchar(100)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', NULL, 2, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (227, 16, 'type', '模块类型 (1: 接口模块, 2: 套件模块, 3: UI模块)', 'enum(\'0\',\'1\',\'2\',\'3\')', 'str', 'type', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 3, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (228, 16, 'parent_id', '父id', 'bigint(20)', 'int', 'parentId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 4, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (230, 16, 'ancestors', '祖级列表', 'varchar(50)', 'str', 'ancestors', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', NULL, 5, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (231, 16, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', NULL, 6, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (232, 16, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'datetime', NULL, 7, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (233, 16, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'input', NULL, 8, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (234, 16, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'datetime', NULL, 9, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (235, 16, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', NULL, 10, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (236, 16, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 11, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (237, 16, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', NULL, 12, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (238, 16, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', NULL, 13, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (254, 18, 'id', '缓存数据ID', 'int(11)', 'int', 'id', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (255, 18, 'cache_key', '缓存键名', 'varchar(255)', 'str', 'cacheKey', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (256, 18, 'environment_id', '关联的环境ID', 'int(11)', 'int', 'environmentId', '0', '0', '0', NULL, '1', '1', '0', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (257, 18, 'cache_value', '缓存值', 'text', 'str', 'cacheValue', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 4, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (258, 18, 'source_type', '数据来源可以为空', 'varchar(50)', 'str', 'sourceType', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 5, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (259, 18, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 6, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (260, 18, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'datetime', '', 7, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (261, 18, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'input', '', 8, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (262, 18, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'datetime', '', 9, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (263, 18, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '0', '0', '0', NULL, 'EQ', 'input', '', 10, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (264, 18, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 11, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (265, 18, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '0', '0', '0', '0', 'EQ', 'input', '', 12, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (266, 18, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (267, 18, 'user_id', '用戶id', 'varchar(255)', 'str', 'userId', '0', '0', '0', NULL, '1', '1', '0', '1', 'EQ', 'input', '', 14, 'admin', '2025-08-02 01:05:33', 'admin', '2025-08-02 01:06:50', NULL, NULL, NULL, 0);
INSERT INTO `gen_table_column` VALUES (349, 16, 'project_id', '所属项目id', 'bigint(20)', 'int', 'projectId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-08-03 13:50:20', 'admin', '2025-08-03 13:52:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (350, 22, 'assertion_id', '断言ID', 'int(11)', 'int', 'assertionId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (351, 22, 'case_id', '关联的测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (352, 22, 'jsonpath', 'JSONPath表达式OR提取方法', 'varchar(255)', 'str', 'jsonpath', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (353, 22, 'jsonpath_index', 'JSONPath提取索引', 'varchar(255)', 'str', 'jsonpathIndex', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (354, 22, 'assertion_method', '断言 (==, !=, >等)', 'varchar(255)', 'str', 'assertionMethod', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (355, 22, 'value', '预期值', 'varchar(255)', 'str', 'value', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (356, 22, 'assert_type', '断言类型 (可选)', 'varchar(255)', 'str', 'assertType', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (357, 22, 'is_run', '是否执行该断言', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (358, 22, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (359, 22, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 10, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (360, 22, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 11, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (361, 22, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 12, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (362, 22, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (363, 22, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (364, 22, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 15, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (365, 22, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 16, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:48', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (366, 23, 'cookie_id', 'ID', 'int(11)', 'int', 'cookieId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (367, 23, 'case_id', '关联的测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (368, 23, 'key', 'Cookie键名', 'varchar(255)', 'str', 'key', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (369, 23, 'value', 'Cookie值', 'text', 'str', 'value', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 4, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (370, 23, 'domain', '作用域', 'varchar(255)', 'str', 'domain', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (371, 23, 'path', '路径', 'varchar(255)', 'str', 'path', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (372, 23, 'is_run', '是否启用该Cookie', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (373, 23, 'description', '描述', 'varchar(255)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (374, 23, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (375, 23, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 10, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (376, 23, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 11, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (377, 23, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 12, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (378, 23, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (379, 23, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (380, 23, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 15, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:03:54', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (381, 24, 'header_id', 'ID', 'int(11)', 'int', 'headerId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (382, 24, 'case_id', '关联的测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (383, 24, 'key', '请求头键名', 'varchar(255)', 'str', 'key', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (384, 24, 'value', '请求头值', 'text', 'str', 'value', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 4, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (385, 24, 'is_run', '是否启用该请求头', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (386, 24, 'description', '描述', 'varchar(255)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (387, 24, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 7, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (388, 24, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 8, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (389, 24, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (390, 24, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 10, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (391, 24, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 11, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (392, 24, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (393, 24, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:10', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (394, 25, 'param_id', 'ID', 'int(11)', 'int', 'paramId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (395, 25, 'case_id', '关联的测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (396, 25, 'key', '参数键名', 'varchar(255)', 'str', 'key', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (397, 25, 'value', '参数值', 'text', 'str', 'value', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 4, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (398, 25, 'is_run', '是否启用该参数', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (399, 25, 'description', '描述', 'varchar(255)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (400, 25, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 7, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (401, 25, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 8, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (402, 25, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (403, 25, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 10, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (404, 25, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 11, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (405, 25, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (406, 25, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:32', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (407, 26, 'setup_id', '操作ID', 'int(11)', 'int', 'setupId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (408, 26, 'name', '操作名称', 'varchar(255)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (409, 26, 'case_id', '关联的测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (410, 26, 'setup_type', '操作类型 (db_connection, execute_script, wait_time)', 'varchar(255)', 'str', 'setupType', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'select', '', 4, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (411, 26, 'db_connection_id', '数据库连接ID', 'int(11)', 'int', 'dbConnectionId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (412, 26, 'script', '脚本语句', 'text', 'str', 'script', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 6, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (413, 26, 'jsonpath', 'jsonpath提取表达式', 'text', 'str', 'jsonpath', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 7, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (414, 26, 'variable_name', '变量名称（用于存储提取的数据）', 'varchar(255)', 'str', 'variableName', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 8, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (415, 26, 'wait_time', '等待时间（毫秒）', 'int(11)', 'int', 'waitTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 9, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (416, 26, 'extract_index', '提取索引', 'int(11)', 'int', 'extractIndex', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 10, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (417, 26, 'extract_index_is_run', '是否执行提取索引操作', 'tinyint(1)', 'int', 'extractIndexIsRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 11, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (418, 26, 'is_run', '是否执行该前置操作', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (419, 26, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (420, 26, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 14, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (421, 26, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 15, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (422, 26, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 16, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (423, 26, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 17, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (424, 26, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 18, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (425, 26, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 19, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (426, 26, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 20, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:04:51', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (427, 27, 'teardown_id', '操作ID', 'int(11)', 'int', 'teardownId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (428, 27, 'name', '操作名称', 'varchar(255)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (429, 27, 'case_id', '关联的测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (430, 27, 'teardown_type', '操作类型 (extract_variable, db_operation, custom_script, wait_time)', 'varchar(255)', 'str', 'teardownType', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (431, 27, 'extract_variable_method', '提取响应的方法： response_textresponse_jsonresponse_xmlresponse_headerresponse_cookie', 'varchar(255)', 'str', 'extractVariableMethod', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (432, 27, 'jsonpath', 'jsonpath提取表达式（用于提取变量）', 'text', 'str', 'jsonpath', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 6, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (433, 27, 'extract_index', '提取索引', 'int(11)', 'int', 'extractIndex', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (434, 27, 'extract_index_is_run', '是否执行提取索引操作', 'tinyint(1)', 'int', 'extractIndexIsRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (435, 27, 'variable_name', '变量名称（用于存储提取的数据）', 'varchar(255)', 'str', 'variableName', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 9, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (436, 27, 'database_id', '数据库连接ID', 'int(11)', 'int', 'databaseId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 10, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (437, 27, 'db_operation', '数据库操作语句（用于数据库操作）', 'text', 'str', 'dbOperation', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 11, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (438, 27, 'script', '自定义脚本语句（用于自定义脚本）', 'text', 'str', 'script', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 12, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (439, 27, 'wait_time', '等待时间（毫秒，用于等待时间）', 'int(11)', 'int', 'waitTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 13, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (440, 27, 'is_run', '是否执行该后置操作', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (441, 27, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 15, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (442, 27, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 16, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (443, 27, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 17, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (444, 27, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 18, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (445, 27, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 19, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (446, 27, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 20, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (447, 27, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 21, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (448, 27, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 22, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:05:22', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (449, 28, 'case_id', '测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '0', NULL, '1', '0', '0', '0', 'EQ', 'input', '', 1, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (450, 28, 'name', '测试用例名称', 'varchar(255)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (451, 28, 'case_type', '测试用例类型 (1接口, 2用例等)', 'varchar(50)', 'str', 'caseType', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'select', 'api_case_type', 3, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (452, 28, 'copy_id', '复制过来的接口用例ID', 'varchar(50)', 'str', 'copyId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (453, 28, 'parent_case_id', '父级测试接口ID', 'int(11)', 'int', 'parentCaseId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (454, 28, 'parent_submodule_id', '父级模块ID', 'int(11)', 'int', 'parentSubmoduleId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (455, 28, 'description', '测试接口/用例描述', 'text', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 7, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (456, 28, 'path', '请求路径', 'varchar(255)', 'str', 'path', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (457, 28, 'method', '请求方法 (GET, POST等)', 'varchar(255)', 'str', 'method', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', 'api_request_method', 9, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (458, 28, 'request_type', '请求类型 (1-None,2-Form Data,3-x-www-form-urlencoded,4-JSON, 5-xml,6-Raw,7-Binary,8-File)', 'varchar(255)', 'str', 'requestType', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'select', 'api_body_type', 10, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (459, 28, 'is_run', '是否执行', 'smallint(6)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 11, 'admin', '2025-08-03 21:52:24', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (460, 28, 'status_code', '预期状态码', 'int(11)', 'int', 'statusCode', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (461, 28, 'sleep', '执行前等待时间 (毫秒)', 'int(11)', 'int', 'sleep', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 13, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (462, 28, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 14, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (463, 28, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 15, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (464, 28, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 16, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (465, 28, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 17, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (466, 28, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 18, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (467, 28, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 19, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (468, 28, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 20, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (469, 28, 'data', '请求数据', 'text', 'str', 'data', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 21, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (470, 28, 'file_path', '文件路径(用于文件上传)', 'varchar(512)', 'str', 'filePath', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 22, 'admin', '2025-08-03 21:52:25', 'admin', '2025-08-03 22:43:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (484, 30, 'formdata_id', 'ID', 'int(11)', 'int', 'formdataId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (485, 30, 'case_id', '关联的测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '0', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (486, 30, 'key', '键名', 'varchar(255)', 'str', 'key', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (487, 30, 'value', '表单值', 'text', 'str', 'value', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'textarea', '', 4, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (488, 30, 'is_run', '是否启用该表单值', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 5, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (489, 30, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 6, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (490, 30, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'datetime', '', 7, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (491, 30, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'input', '', 8, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (492, 30, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '0', '0', NULL, NULL, 'EQ', 'datetime', '', 9, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (493, 30, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '0', '0', '0', NULL, 'EQ', 'input', '', 10, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (494, 30, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 11, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (495, 30, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 12, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (496, 30, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-06 20:12:05', 'admin', '2025-08-06 20:13:52', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (497, 31, 'file_id', '（主键）', 'int(11)', 'int', 'fileId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (498, 31, 'original_name', '文件原始名称', 'varchar(255)', 'str', 'originalName', '0', '0', '0', NULL, '1', '1', '0', '0', 'LIKE', 'input', '', 2, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (499, 31, 'stored_name', '文件存储名称', 'varchar(191)', 'str', 'storedName', '0', '0', '1', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 3, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (500, 31, 'file_ext', '文件扩展名', 'varchar(50)', 'str', 'fileExt', '0', '0', '0', NULL, '1', '1', '0', '0', 'EQ', 'input', '', 4, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (501, 31, 'mime_type', '文件 MIME 类型', 'varchar(100)', 'str', 'mimeType', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 5, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (502, 31, 'file_size', '文件大小（字节）', 'bigint(20)', 'int', 'fileSize', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 6, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (503, 31, 'file_path', '文件存储路径', 'text', 'str', 'filePath', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'textarea', '', 7, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (504, 31, 'file_url', '文件访问 URL', 'text', 'str', 'fileUrl', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'textarea', '', 8, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (505, 31, 'storage_type', '存储位置类型', 'varchar(50)', 'str', 'storageType', '0', '0', '0', NULL, '1', '1', '0', '0', 'EQ', 'input', '', 9, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (506, 31, 'is_temp', '是否临时文件', 'tinyint(1)', 'int', 'isTemp', '0', '0', '0', NULL, '1', '1', '0', '0', 'EQ', 'input', '', 10, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (507, 31, 'file_hash', '文件哈希值', 'varchar(128)', 'str', 'fileHash', '0', '0', '0', NULL, '1', '1', '0', '0', 'EQ', 'input', '', 11, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (508, 31, 'biz_tag', '业务标签', 'varchar(100)', 'str', 'bizTag', '0', '0', '0', NULL, '1', '1', '0', '0', 'EQ', 'input', '', 12, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (509, 31, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (510, 31, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 14, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (511, 31, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 15, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (512, 31, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 16, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (513, 31, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '0', NULL, 'EQ', 'input', '', 17, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (514, 31, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '0', '0', 'EQ', 'input', '', 18, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (515, 31, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '0', '1', '0', '0', 'EQ', 'input', '', 19, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (516, 31, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 20, 'admin', '2025-08-22 14:56:08', 'admin', '2025-08-22 15:37:37', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (517, 32, 'workflow_id', '执行器ID', 'varchar(50)', 'str', 'workflowId', '1', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (518, 32, 'name', '执行器名称', 'varchar(200)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (519, 32, 'execution_config', '执行配置', 'json', 'dict', 'executionConfig', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 3, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (520, 32, 'parent_submodule_id', '父级模块ID', 'bigint(20)', 'int', 'parentSubmoduleId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (521, 32, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, '1', NULL, 'EQ', 'input', '', 5, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (522, 32, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, '1', NULL, 'EQ', 'datetime', '', 6, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (523, 32, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '0', '1', NULL, 'EQ', 'input', '', 7, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (524, 32, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '0', '1', NULL, 'EQ', 'datetime', '', 8, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (525, 32, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (526, 32, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 10, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (527, 32, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 11, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (528, 32, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 12, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:51:53', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (529, 33, 'workflow_execution_id', '执行记录ID', 'int(11)', 'int', 'workflowExecutionId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (530, 33, 'workflow_id', '执行器ID', 'varchar(50)', 'str', 'workflowId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (531, 33, 'workflow_name', '执行名称', 'varchar(200)', 'str', 'workflowName', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 3, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (532, 33, 'status', '执行状态', 'varchar(20)', 'str', 'status', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 4, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (533, 33, 'start_time', '开始时间', 'datetime', 'datetime', 'startTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 5, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (534, 33, 'end_time', '结束时间', 'datetime', 'datetime', 'endTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 6, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (535, 33, 'duration', '执行时长(秒)', 'int(11)', 'int', 'duration', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (536, 33, 'input_data', '输入数据', 'json', 'dict', 'inputData', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 8, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (537, 33, 'output_data', '输出数据', 'json', 'dict', 'outputData', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 9, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (538, 33, 'context_data', '上下文数据', 'json', 'dict', 'contextData', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 10, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (539, 33, 'total_nodes', '总节点数', 'int(11)', 'int', 'totalNodes', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 11, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (540, 33, 'success_nodes', '成功节点数', 'int(11)', 'int', 'successNodes', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (541, 33, 'failed_nodes', '失败节点数', 'int(11)', 'int', 'failedNodes', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 13, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (542, 33, 'skipped_nodes', '跳过节点数', 'int(11)', 'int', 'skippedNodes', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (543, 33, 'error_message', '错误信息', 'text', 'str', 'errorMessage', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 15, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (544, 33, 'error_details', '错误详情', 'json', 'dict', 'errorDetails', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 16, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (545, 33, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 17, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (546, 33, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 18, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (547, 33, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 19, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (548, 33, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 20, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (549, 33, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 21, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (550, 33, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 22, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (551, 33, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 23, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (552, 33, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 24, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:54:19', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (553, 34, 'schemas_id', 'Schema配置ID', 'int(11)', 'int', 'schemasId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (554, 34, 'schema_version', 'Schema版本', 'varchar(20)', 'str', 'schemaVersion', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (555, 34, 'node_types', '节点类型定义', 'json', 'dict', 'nodeTypes', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 3, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (556, 34, 'condition_operators', '条件操作符列表', 'json', 'dict', 'conditionOperators', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 4, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (557, 34, 'error_handling_options', '错误处理选项', 'json', 'dict', 'errorHandlingOptions', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 5, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (558, 34, 'custom_config', '自定义配置', 'json', 'dict', 'customConfig', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 6, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (559, 34, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 7, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (560, 34, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 8, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (561, 34, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (562, 34, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 10, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (563, 34, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 11, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (564, 34, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (565, 34, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 13, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (566, 34, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 14, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 15:12:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (567, 35, 'node_execution_id', '节点执行记录ID', 'int(11)', 'int', 'nodeExecutionId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (568, 35, 'workflow_execution_id', '执行器执行记录ID', 'int(11)', 'int', 'workflowExecutionId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (569, 35, 'node_id', '节点ID', 'varchar(50)', 'str', 'nodeId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (570, 35, 'status', '执行状态', 'varchar(20)', 'str', 'status', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'radio', '', 4, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (571, 35, 'start_time', '开始时间', 'datetime', 'datetime', 'startTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 5, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (572, 35, 'end_time', '结束时间', 'datetime', 'datetime', 'endTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 6, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (573, 35, 'duration', '执行时长(毫秒)', 'int(11)', 'int', 'duration', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (574, 35, 'input_data', '输入数据', 'json', 'dict', 'inputData', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 8, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (575, 35, 'output_data', '输出数据', 'json', 'dict', 'outputData', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 9, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (576, 35, 'context_snapshot', '执行时上下文快照', 'json', 'dict', 'contextSnapshot', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 10, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (577, 35, 'loop_index', '循环索引', 'int(11)', 'int', 'loopIndex', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 11, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (578, 35, 'loop_item', '循环项数据', 'json', 'dict', 'loopItem', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 12, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (579, 35, 'condition_result', '条件判断结果', 'tinyint(1)', 'int', 'conditionResult', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 13, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (580, 35, 'error_message', '错误信息', 'text', 'str', 'errorMessage', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 14, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (581, 35, 'error_details', '错误详情', 'json', 'dict', 'errorDetails', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 15, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (582, 35, 'retry_count', '重试次数', 'int(11)', 'int', 'retryCount', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 16, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (583, 35, 'created_at', '创建时间', 'datetime', 'datetime', 'createdAt', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 17, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (584, 35, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 18, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (585, 35, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 19, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (586, 35, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 20, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (587, 35, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 21, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (588, 35, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 22, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (589, 35, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 23, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (590, 35, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 24, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (591, 35, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 25, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:20:20', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (592, 36, 'node_id', '节点ID', 'varchar(50)', 'str', 'nodeId', '1', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (593, 36, 'workflow_id', '所属执行器ID', 'varchar(50)', 'str', 'workflowId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (594, 36, 'parent_id', '父节点ID', 'varchar(50)', 'str', 'parentId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (595, 36, 'name', '节点名称', 'varchar(200)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 4, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (596, 36, 'type', '节点类型', 'enum(\'IF\',\'ELSE\',\'FOR\',\'FOREACH\',\'GROUP\',\'TASK\')', 'str', 'type', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (597, 36, 'is_run', '是否启用执行', 'tinyint(1)', 'int', 'isRun', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (598, 36, 'children_ids', '子结点列表', 'json', 'dict', 'childrenIds', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 7, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (599, 36, 'config', '节点配置信息', 'json', 'dict', 'config', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 8, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (600, 36, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 9, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (601, 36, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 10, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (602, 36, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 11, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (603, 36, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 12, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (604, 36, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 13, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (605, 36, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 14, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (606, 36, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 15, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (607, 36, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '0', NULL, NULL, NULL, 'EQ', 'input', '', 16, 'admin', '2025-08-28 15:12:17', 'admin', '2025-08-28 16:30:44', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (608, 37, 'log_id', '执行日志ID', 'int(11)', 'int', 'logId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (609, 37, 'case_id', '测试用例ID', 'int(11)', 'int', 'caseId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (610, 37, 'case_name', '测试用例名称', 'varchar(255)', 'str', 'caseName', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 3, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (611, 37, 'execution_time', '执行时间', 'datetime', 'datetime', 'executionTime', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 4, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (612, 37, 'is_success', '是否执行成功', 'tinyint(1)', 'int', 'isSuccess', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 5, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (613, 37, 'execution_data', '完整执行数据', 'json', 'dict', 'executionData', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 6, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (614, 37, 'response_status_code', '响应状态码', 'int(11)', 'int', 'responseStatusCode', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (615, 37, 'response_time', '响应时间(秒)', 'float', 'float', 'responseTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (616, 37, 'assertion_success', '断言是否成功', 'tinyint(1)', 'int', 'assertionSuccess', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 9, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (617, 37, 'project_id', '项目ID', 'int(11)', 'int', 'projectId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 10, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (618, 37, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, '1', NULL, 'EQ', 'input', '', 11, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (619, 37, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, '1', NULL, 'EQ', 'datetime', '', 12, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (620, 37, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 13, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (621, 37, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'datetime', '', 14, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (622, 37, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 15, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (623, 37, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 16, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (624, 37, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 17, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (625, 37, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, '1', NULL, 'EQ', 'input', '', 18, 'admin', '2025-11-02 22:46:57', 'admin', '2025-11-02 22:49:17', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (626, 38, 'key_id', '主键ID', 'bigint(20)', 'int', 'keyId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (627, 38, 'parameterization_id', '所属参数表ID', 'bigint(20)', 'int', 'parameterizationId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (628, 38, 'group_name', '参数分组', 'varchar(100)', 'str', 'groupName', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 3, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (629, 38, 'key', '参数键', 'varchar(100)', 'str', 'key', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 4, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (630, 38, 'value', '参数值', 'text', 'str', 'value', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'textarea', '', 5, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (631, 38, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 6, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (632, 38, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 7, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (633, 38, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 8, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (634, 38, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 9, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (635, 38, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 10, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (636, 38, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 11, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (637, 38, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (638, 38, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:23:58', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (639, 39, 'parameterization_id', '主键ID', 'bigint(20)', 'int', 'parameterizationId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (640, 39, 'workflow_id', '所属执行器ID', 'bigint(20)', 'int', 'workflowId', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (641, 39, 'name', '参数表名称', 'varchar(100)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 3, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (642, 39, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 4, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (643, 39, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 5, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (644, 39, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 6, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (645, 39, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 7, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (646, 39, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 8, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (647, 39, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 9, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (648, 39, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 10, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (649, 39, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 11, 'admin', '2025-11-13 22:14:03', 'admin', '2025-11-13 22:21:29', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (650, 40, 'report_id', '报告ID', 'bigint(20)', 'int', 'reportId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (651, 40, 'workflow_id', '执行器ID', 'bigint(20)', 'int', 'workflowId', '0', '0', '1', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 2, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (652, 40, 'name', '报告名称', 'varchar(255)', 'str', 'name', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 3, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (653, 40, 'start_time', '开始时间', 'datetime', 'datetime', 'startTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 4, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (654, 40, 'end_time', '结束时间', 'datetime', 'datetime', 'endTime', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'datetime', '', 5, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (655, 40, 'total_cases', '总用例数', 'int(11)', 'int', 'totalCases', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 6, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (656, 40, 'success_cases', '成功用例数', 'int(11)', 'int', 'successCases', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 7, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (657, 40, 'failed_cases', '失败用例数', 'int(11)', 'int', 'failedCases', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 8, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (658, 40, 'duration', '总耗时(秒)', 'float', 'float', 'duration', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 9, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (659, 40, 'is_success', '是否全部成功', 'tinyint(1)', 'int', 'isSuccess', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 10, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (660, 40, 'report_data', '完整报告JSON数据', 'json', 'dict', 'reportData', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', NULL, '', 11, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (661, 40, 'trigger_type', '触发类型', 'enum(\'manual\',\'cron\',\'api\',\'system\')', 'str', 'triggerType', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'select', '', 12, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (662, 40, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (663, 40, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 14, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (664, 40, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'input', '', 15, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (665, 40, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '1', NULL, NULL, 'EQ', 'datetime', '', 16, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (666, 40, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '1', '1', NULL, 'EQ', 'input', '', 17, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (667, 40, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 18, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (668, 40, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'input', '', 19, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (669, 40, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 20, 'admin', '2025-11-30 17:47:27', 'admin', '2025-11-30 17:56:09', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (670, 41, 'notification_id', '通知ID', 'bigint(20)', 'int', 'notificationId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (671, 41, 'user_id', '接收用户ID', 'bigint(20)', 'int', 'userId', '0', '0', '1', NULL, '1', '0', '0', '0', 'EQ', 'input', '', 2, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (672, 41, 'notification_type', '通知类型(system/task/workflow/alert)', 'enum(\'SUCCESS\',\'ERROR\',\'ALERT\')', 'str', 'notificationType', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'select', '', 3, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (673, 41, 'title', '通知标题', 'varchar(200)', 'str', 'title', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 4, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (674, 41, 'message', '通知内容', 'text', 'str', 'message', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'textarea', '', 5, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (675, 41, 'is_read', '是否已读', 'tinyint(1)', 'int', 'isRead', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'input', '', 6, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (676, 41, 'read_time', '阅读时间', 'datetime', 'datetime', 'readTime', '0', '0', '0', NULL, '1', '1', '1', '0', 'EQ', 'datetime', '', 7, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (677, 41, 'business_type', '关联业务类型(workflow/test_case/report等)', 'varchar(50)', 'str', 'businessType', '0', '0', '0', NULL, '1', '0', '0', '0', 'EQ', 'select', '', 8, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (678, 41, 'business_id', '关联业务ID', 'bigint(20)', 'int', 'businessId', '0', '0', '0', NULL, '1', '0', '0', '0', 'EQ', 'input', '', 9, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (679, 41, 'extra_data', '扩展数据', 'json', 'dict', 'extraData', '0', '0', '0', NULL, '1', '0', '0', '0', 'EQ', NULL, '', 10, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (680, 41, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 11, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (681, 41, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, '1', 'EQ', 'datetime', '', 12, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (682, 41, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '0', NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (683, 41, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '0', NULL, NULL, 'EQ', 'datetime', '', 14, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (684, 41, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '0', '0', NULL, 'EQ', 'input', '', 15, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (685, 41, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '0', '0', '0', 'EQ', 'input', '', 16, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (686, 41, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '0', '0', '0', 'EQ', 'input', '', 17, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (687, 41, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 18, 'admin', '2025-12-03 16:25:32', 'admin', '2025-12-03 20:54:38', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (688, 42, 'script_id', '脚本ID', 'bigint(20)', 'int', 'scriptId', '1', '1', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 1, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (689, 42, 'script_name', '脚本名称', 'varchar(100)', 'str', 'scriptName', '0', '0', '0', NULL, '1', '1', '1', '1', 'LIKE', 'input', '', 2, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (690, 42, 'script_type', '脚本类型(python/javascript)', 'enum(\'python\',\'javascript\')', 'str', 'scriptType', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'select', '', 3, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (691, 42, 'script_content', '脚本内容', 'text', 'str', 'scriptContent', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'editor', '', 4, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (692, 42, 'status', '状态(0停用 1正常)', 'int(11)', 'int', 'status', '0', '0', '0', NULL, '1', '1', '1', '1', 'EQ', 'radio', '', 5, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (693, 42, 'create_by', '创建者', 'varchar(64)', 'str', 'createBy', '0', '0', '0', NULL, '1', '0', NULL, NULL, 'EQ', 'input', '', 6, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (694, 42, 'create_time', '创建时间', 'datetime', 'datetime', 'createTime', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'datetime', '', 7, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (695, 42, 'update_by', '更新者', 'varchar(64)', 'str', 'updateBy', '0', '0', '0', NULL, '1', '0', NULL, NULL, 'EQ', 'input', '', 8, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (696, 42, 'update_time', '更新时间', 'datetime', 'datetime', 'updateTime', '0', '0', '0', NULL, '1', '0', NULL, NULL, 'EQ', 'datetime', '', 9, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (697, 42, 'remark', '备注', 'varchar(500)', 'str', 'remark', '0', '0', '0', NULL, '1', '0', '1', NULL, 'EQ', 'input', '', 10, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (698, 42, 'description', '描述', 'varchar(500)', 'str', 'description', '0', '0', '0', NULL, '1', '0', '1', '1', 'EQ', 'input', '', 11, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (699, 42, 'sort_no', '排序值', 'float', 'float', 'sortNo', '0', '0', '0', NULL, '1', '0', '1', '1', 'EQ', 'input', '', 12, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);
INSERT INTO `gen_table_column` VALUES (700, 42, 'del_flag', '删除标志 0正常 1删除 2代表删除', 'int(11)', 'int', 'delFlag', '0', '0', '0', NULL, '1', NULL, NULL, NULL, 'EQ', 'input', '', 13, 'admin', '2025-12-13 17:19:38', 'admin', '2025-12-13 17:57:15', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS `sys_config`;
CREATE TABLE `sys_config`  (
  `config_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '参数主键',
  `config_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参数名称',
  `config_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参数键名',
  `config_value` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '参数键值',
  `config_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '系统内置（Y是 N否）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`config_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_config
-- ----------------------------
INSERT INTO `sys_config` VALUES (1, '主框架页-默认皮肤样式名称', 'sys.index.skinName', 'skin-blue', 'Y', 'admin', '2025-07-02 16:37:32', '', NULL, '蓝色 skin-blue、绿色 skin-green、紫色 skin-purple、红色 skin-red、黄色 skin-yellow', NULL, NULL, NULL);
INSERT INTO `sys_config` VALUES (2, '用户管理-账号初始密码', 'sys.user.initPassword', '123456', 'Y', 'admin', '2025-07-02 16:37:32', '', NULL, '初始化密码 123456', NULL, NULL, NULL);
INSERT INTO `sys_config` VALUES (3, '主框架页-侧边栏主题', 'sys.index.sideTheme', 'theme-light', 'Y', 'admin', '2025-07-02 16:37:32', 'admin', '2025-08-10 18:46:35', '深色主题theme-dark，浅色主题theme-light', NULL, NULL, NULL);
INSERT INTO `sys_config` VALUES (4, '账号自助-验证码开关', 'sys.account.captchaEnabled', 'false', 'Y', 'admin', '2025-07-02 16:37:32', 'admin', '2025-07-03 09:13:26', '是否开启验证码功能（true开启，false关闭）', NULL, NULL, NULL);
INSERT INTO `sys_config` VALUES (5, '账号自助-是否开启用户注册功能', 'sys.account.registerUser', 'true', 'Y', 'admin', '2025-07-02 16:37:32', 'admin', '2025-07-03 09:13:18', '是否开启注册用户功能（true开启，false关闭）', NULL, NULL, NULL);
INSERT INTO `sys_config` VALUES (6, '用户登录-黑名单列表', 'sys.login.blackIPList', '', 'Y', 'admin', '2025-07-02 16:37:32', '', NULL, '设置登录IP黑名单限制，多个匹配项以;分隔，支持匹配（*通配、网段）', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for sys_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_dept`;
CREATE TABLE `sys_dept`  (
  `dept_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '部门id',
  `parent_id` int(11) NULL DEFAULT NULL COMMENT '父部门id',
  `ancestors` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '祖级列表',
  `dept_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '部门名称',
  `order_num` int(11) NULL DEFAULT NULL COMMENT '显示顺序',
  `leader` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '负责人',
  `phone` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '联系电话',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '邮箱',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '部门状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`dept_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 112 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dept
-- ----------------------------
INSERT INTO `sys_dept` VALUES (100, 0, '0', '集团总公司', 0, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (101, 100, '0,100', '深圳分公司', 1, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (102, 100, '0,100', '长沙分公司', 2, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (103, 101, '0,100,101', '研发部门', 1, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (104, 101, '0,100,101', '市场部门', 2, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (105, 101, '0,100,101', '测试部门', 3, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (106, 101, '0,100,101', '财务部门', 4, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (107, 101, '0,100,101', '运维部门', 5, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (108, 102, '0,100,102', '市场部门', 1, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', '', NULL, NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (109, 102, '0,100,102', '财务部门', 2, '年糕', '15888888888', 'niangao@qq.com', '0', 'admin', '2025-07-02 16:37:31', 'admin', '2025-07-30 11:34:25', NULL, NULL, NULL, 0);
INSERT INTO `sys_dept` VALUES (110, 109, '0,100,102,109', '111', 0, NULL, NULL, NULL, '0', 'admin', '2025-07-08 15:03:48', NULL, NULL, NULL, NULL, NULL, 2);
INSERT INTO `sys_dept` VALUES (111, 109, '0,100,102,109', '测试部门', 0, NULL, NULL, NULL, '0', 'admin', '2025-07-31 00:07:24', 'admin', '2025-07-31 00:07:24', NULL, NULL, NULL, 0);

-- ----------------------------
-- Table structure for sys_dict_data
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_data`;
CREATE TABLE `sys_dict_data`  (
  `dict_code` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '字典编码',
  `dict_sort` int(11) NULL DEFAULT NULL COMMENT '字典排序',
  `dict_label` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字典标签',
  `dict_value` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字典键值',
  `dict_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字典类型',
  `css_class` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '样式属性（其他样式扩展）',
  `list_class` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '表格回显样式',
  `is_default` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否默认（Y是 N否）',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`dict_code`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 71 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict_data
-- ----------------------------
INSERT INTO `sys_dict_data` VALUES (1, 1, '男', '0', 'sys_user_sex', '', '', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '性别男', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (2, 2, '女', '1', 'sys_user_sex', '', '', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '性别女', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (3, 3, '未知', '2', 'sys_user_sex', '', '', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '性别未知', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (4, 1, '显示', '0', 'sys_show_hide', '', 'primary', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '显示菜单', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (5, 2, '隐藏', '1', 'sys_show_hide', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '隐藏菜单', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (6, 1, '正常', '0', 'sys_normal_disable', '', 'primary', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '正常状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (7, 2, '停用', '1', 'sys_normal_disable', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '停用状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (8, 1, '正常', '0', 'sys_job_status', '', 'primary', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '正常状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (9, 2, '暂停', '1', 'sys_job_status', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '停用状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (10, 1, '默认', 'default', 'sys_job_group', '', '', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '默认分组', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (11, 2, '数据库', 'sqlalchemy', 'sys_job_group', '', '', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '数据库分组', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (12, 3, 'redis', 'redis', 'sys_job_group', '', '', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, 'reids分组', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (13, 1, '默认', 'default', 'sys_job_executor', '', '', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '线程池', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (14, 2, '进程池', 'processpool', 'sys_job_executor', '', '', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '进程池', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (15, 1, '是', 'Y', 'sys_yes_no', '', 'primary', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '系统默认是', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (16, 2, '否', 'N', 'sys_yes_no', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '系统默认否', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (17, 1, '通知', '1', 'sys_notice_type', '', 'warning', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '通知', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (18, 2, '公告', '2', 'sys_notice_type', '', 'success', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '公告', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (19, 1, '正常', '0', 'sys_notice_status', '', 'primary', 'Y', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '正常状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (20, 2, '关闭', '1', 'sys_notice_status', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '关闭状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (21, 99, '其他', '0', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '其他操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (22, 1, '新增', '1', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '新增操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (23, 2, '修改', '2', 'sys_oper_type', '', 'info', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '修改操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (24, 3, '删除', '3', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '删除操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (25, 4, '授权', '4', 'sys_oper_type', '', 'primary', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '授权操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (26, 5, '导出', '5', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '导出操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (27, 6, '导入', '6', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '导入操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (28, 7, '强退', '7', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '强退操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (29, 8, '生成代码', '8', 'sys_oper_type', '', 'warning', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '生成操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (30, 9, '清空数据', '9', 'sys_oper_type', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '清空操作', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (31, 1, '成功', '0', 'sys_common_status', '', 'primary', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '正常状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (32, 2, '失败', '1', 'sys_common_status', '', 'danger', 'N', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '停用状态', NULL, NULL, NULL);
INSERT INTO `sys_dict_data` VALUES (33, 0, '正常', '0', 'sys_del_flag', NULL, 'default', 'N', '0', 'admin', '2025-07-29 15:09:38', 'admin', '2025-07-29 16:31:28', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (34, 0, '删除', '1', 'sys_del_flag', NULL, 'default', 'N', '0', 'admin', '2025-07-29 15:09:47', 'admin', '2025-07-29 16:31:36', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (36, 1, 'mysql数据库', '1', 'database_type', NULL, 'warning', 'N', '0', 'admin', '2025-07-30 17:30:15', 'admin', '2025-07-31 09:55:23', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (37, 0, 'redis数据库', '2', 'database_type', NULL, 'primary', 'N', '0', 'admin', '2025-07-30 17:30:24', 'admin', '2025-07-31 09:55:16', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (38, 1, '默认', '1', 'user_is_defalut', NULL, 'primary', 'N', '0', 'admin', '2025-07-30 23:26:21', 'admin', '2025-07-30 23:27:29', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (39, 0, '否', '0', 'user_is_defalut', NULL, 'info', 'N', '0', 'admin', '2025-07-30 23:26:32', 'admin', '2025-07-30 23:27:49', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (40, 0, 'POST', 'POST', 'api_request_method', NULL, 'primary', 'N', '0', 'admin', '2025-08-03 01:58:06', 'admin', '2025-08-03 02:01:16', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (41, 0, 'GET', 'GET', 'api_request_method', NULL, 'success', 'N', '0', 'admin', '2025-08-03 01:58:06', 'admin', '2025-08-03 02:01:21', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (42, 0, 'PUT', 'PUT', 'api_request_method', NULL, 'warning', 'N', '0', 'admin', '2025-08-03 01:59:13', 'admin', '2025-08-03 02:01:38', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (43, 0, 'DELETE', 'DELETE', 'api_request_method', NULL, 'danger', 'N', '0', 'admin', '2025-08-03 01:59:19', 'admin', '2025-08-03 02:01:48', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (44, 0, 'OPTIONS', 'OPTIONS', 'api_request_method', NULL, 'info', 'N', '0', 'admin', '2025-08-03 01:59:25', 'admin', '2025-08-03 02:02:00', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (45, 0, 'HEAD', 'HEAD', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 01:59:31', 'admin', '2025-08-03 01:59:31', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (46, 0, 'PATCH', 'PATCH', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 01:59:37', 'admin', '2025-08-03 01:59:37', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (47, 0, 'TRACE', 'TRACE', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 01:59:43', 'admin', '2025-08-03 01:59:43', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (48, 0, 'CONNECT', 'CONNECT', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 01:59:49', 'admin', '2025-08-03 01:59:49', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (49, 0, 'COPY', 'COPY', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 01:59:55', 'admin', '2025-08-03 01:59:55', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (50, 0, 'LINK', 'LINK', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:02', 'admin', '2025-08-03 02:00:02', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (51, 0, 'UNLINK', 'UNLINK', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:08', 'admin', '2025-08-03 02:00:08', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (52, 0, 'PURGE', 'PURGE', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:14', 'admin', '2025-08-03 02:00:14', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (53, 0, 'LOCK', 'LOCK', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:19', 'admin', '2025-08-03 02:00:19', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (54, 0, 'UNLOCK', 'UNLOCK', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:25', 'admin', '2025-08-03 02:00:25', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (55, 0, 'MKCOL', 'MKCOL', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:32', 'admin', '2025-08-03 02:00:32', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (56, 0, 'MOVE', 'MOVE', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:38', 'admin', '2025-08-03 02:00:38', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (57, 0, 'PROPFIND', 'PROPFIND', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:44', 'admin', '2025-08-03 02:00:44', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (58, 0, 'REPORT', 'REPORT', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:50', 'admin', '2025-08-03 02:00:50', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (59, 0, 'VIEW', 'VIEW', 'api_request_method', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:00:57', 'admin', '2025-08-03 02:00:57', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (60, 0, 'NONE', 'NONE', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:02:32', 'admin', '2025-08-03 02:02:32', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (61, 0, 'Form_Data', 'Form_Data', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:02:38', 'admin', '2025-08-03 02:02:38', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (62, 0, 'x_www_form_urlencoded', 'x_www_form_urlencoded', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:02:44', 'admin', '2025-08-03 02:02:44', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (63, 0, 'JSON', 'JSON', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:02:51', 'admin', '2025-08-03 02:02:51', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (64, 0, 'XML', 'XML', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:03:05', 'admin', '2025-08-03 02:03:05', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (65, 0, 'Raw', 'Raw', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:03:11', 'admin', '2025-08-03 02:03:11', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (66, 0, 'Binary', 'Binary', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:03:16', 'admin', '2025-08-03 02:03:16', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (67, 0, 'File', 'File', 'api_body_type', NULL, 'default', 'N', '0', 'admin', '2025-08-03 02:03:22', 'admin', '2025-08-03 02:03:22', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (69, 0, '接口', '1', 'api_case_type', NULL, 'primary', 'N', '0', 'admin', '2025-08-03 02:05:42', 'admin', '2025-08-03 02:05:57', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_data` VALUES (70, 0, '用例', '2', 'api_case_type', NULL, 'success', 'N', '0', 'admin', '2025-08-03 02:05:51', 'admin', '2025-08-03 02:06:01', NULL, NULL, NULL, 0);

-- ----------------------------
-- Table structure for sys_dict_type
-- ----------------------------
DROP TABLE IF EXISTS `sys_dict_type`;
CREATE TABLE `sys_dict_type`  (
  `dict_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '字典主键',
  `dict_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字典名称',
  `dict_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字典类型',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`dict_id`) USING BTREE,
  UNIQUE INDEX `uq_sys_dict_type_dict_type`(`dict_type`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 19 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_dict_type
-- ----------------------------
INSERT INTO `sys_dict_type` VALUES (1, '用户性别', 'sys_user_sex', '0', 'admin', '2025-07-02 16:37:32', 'admin', '2025-07-08 10:29:18', '用户性别列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (2, '菜单状态', 'sys_show_hide', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '菜单状态列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (3, '系统开关', 'sys_normal_disable', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '系统开关列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (4, '任务状态', 'sys_job_status', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '任务状态列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (5, '任务分组', 'sys_job_group', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '任务分组列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (6, '任务执行器', 'sys_job_executor', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '任务执行器列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (7, '系统是否', 'sys_yes_no', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '系统是否列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (8, '通知类型', 'sys_notice_type', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '通知类型列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (9, '通知状态', 'sys_notice_status', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '通知状态列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (10, '操作类型', 'sys_oper_type', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '操作类型列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (11, '系统状态', 'sys_common_status', '0', 'admin', '2025-07-02 16:37:32', '', NULL, '登录状态列表', NULL, NULL, NULL);
INSERT INTO `sys_dict_type` VALUES (12, '是否删除', 'sys_del_flag', '0', 'admin', '2025-07-29 15:09:10', 'admin', '2025-07-29 15:09:10', '系统删除标志', NULL, NULL, 0);
INSERT INTO `sys_dict_type` VALUES (13, '数据库类型', 'database_type', '0', 'admin', '2025-07-30 17:29:55', 'admin', '2025-07-30 17:29:55', '数据库类型', NULL, NULL, 0);
INSERT INTO `sys_dict_type` VALUES (14, '是否默认', 'user_is_defalut', '0', 'admin', '2025-07-30 23:25:28', 'admin', '2025-07-30 23:26:04', '是否默认存在', NULL, NULL, 0);
INSERT INTO `sys_dict_type` VALUES (16, '接口请求方法', 'api_request_method', '0', 'admin', '2025-08-03 01:55:42', 'admin', '2025-08-03 01:55:42', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_type` VALUES (17, '接口请求体类型', 'api_body_type', '0', 'admin', '2025-08-03 01:57:10', 'admin', '2025-08-03 01:57:10', NULL, NULL, NULL, 0);
INSERT INTO `sys_dict_type` VALUES (18, '接口用例类型', 'api_case_type', '0', 'admin', '2025-08-03 02:05:21', 'admin', '2025-08-03 02:05:21', NULL, NULL, NULL, 0);

-- ----------------------------
-- Table structure for sys_file
-- ----------------------------
DROP TABLE IF EXISTS `sys_file`;
CREATE TABLE `sys_file`  (
  `file_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '（主键）',
  `original_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件原始名称',
  `stored_name` varchar(191) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件存储名称',
  `file_ext` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件扩展名',
  `mime_type` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件 MIME 类型',
  `file_size` bigint(20) NULL DEFAULT NULL COMMENT '文件大小（字节）',
  `file_path` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '文件存储路径',
  `file_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '文件访问 URL',
  `storage_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '存储位置类型',
  `is_temp` tinyint(1) NULL DEFAULT NULL COMMENT '是否临时文件',
  `file_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '文件哈希值',
  `biz_tag` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '业务标签',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`file_id`) USING BTREE,
  UNIQUE INDEX `stored_name`(`stored_name`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 177 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '附件表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_file
-- ----------------------------

-- ----------------------------
-- Table structure for sys_job
-- ----------------------------
DROP TABLE IF EXISTS `sys_job`;
CREATE TABLE `sys_job`  (
  `job_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '任务ID',
  `job_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务组名',
  `job_executor` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务执行器',
  `invoke_target` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '调用目标字符串',
  `job_args` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '位置参数',
  `job_kwargs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关键字参数',
  `cron_expression` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'cron执行表达式',
  `misfire_policy` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '计划执行错误策略（1立即执行 2执行一次 3放弃执行）',
  `concurrent` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否并发执行（0允许 1禁止）',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '状态（0正常 1暂停）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`job_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_job
-- ----------------------------
INSERT INTO `sys_job` VALUES (1, '执行工作流3', 'default', 'default', 'module_task.scheduler_test.run_workflow_task', '', '{\"workflow_id\": 1, \"user_id\": 1,\"env_id\":4,\"loop_count\":1,\"parameterization_id\": null}', '0 0/1 * * * ?', '3', '1', '1', 'admin', '2025-07-02 16:37:33', 'admin', '2025-12-23 22:55:56', '', NULL, NULL, NULL);
INSERT INTO `sys_job` VALUES (2, '系统默认（有参）', 'default', 'default', 'module_task.scheduler_test.job', 'test', NULL, '0/15 * * * * ?', '3', '1', '1', 'admin', '2025-07-02 16:37:33', 'admin', '2025-12-22 17:35:42', '', NULL, NULL, NULL);
INSERT INTO `sys_job` VALUES (3, '系统默认（多参）', 'default', 'default', 'module_task.scheduler_test.job', 'new', '{\"test\": 111}', '0/20 * * * * ?', '3', '1', '1', 'admin', '2025-07-02 16:37:33', 'admin', '2025-12-22 17:35:54', '', NULL, NULL, NULL);
INSERT INTO `sys_job` VALUES (4, '执行工作流1', 'default', 'default', 'module_task.scheduler_test.run_workflow_task', '', '{\"workflow_id\": 1, \"user_id\": 1,\"env_id\":1,\"loop_count\":1,\"parameterization_id\": null}', '0 0 0/1 * * ?', '1', '1', '1', 'admin', '2025-12-04 21:56:25', 'admin', '2025-12-22 17:36:38', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for sys_job_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_job_log`;
CREATE TABLE `sys_job_log`  (
  `job_log_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '任务日志ID',
  `job_name` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务名称',
  `job_group` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务组名',
  `job_executor` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '任务执行器',
  `invoke_target` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '调用目标字符串',
  `job_args` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '位置参数',
  `job_kwargs` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '关键字参数',
  `job_trigger` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '任务触发器',
  `job_message` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '日志信息',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '执行状态（0正常 1失败）',
  `exception_info` varchar(2000) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '异常信息',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`job_log_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 26661 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_job_log
-- ----------------------------

-- ----------------------------
-- Table structure for sys_logininfor
-- ----------------------------
DROP TABLE IF EXISTS `sys_logininfor`;
CREATE TABLE `sys_logininfor`  (
  `info_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '访问ID',
  `user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户账号',
  `ipaddr` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录IP地址',
  `login_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录地点',
  `browser` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '浏览器类型',
  `os` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作系统',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '登录状态（0成功 1失败）',
  `msg` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '提示消息',
  `login_time` datetime NULL DEFAULT NULL COMMENT '访问时间',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`info_id`) USING BTREE,
  INDEX `idx_sys_logininfor_lt`(`login_time`) USING BTREE,
  INDEX `idx_sys_logininfor_s`(`status`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 834 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_logininfor
-- ----------------------------
INSERT INTO `sys_logininfor` VALUES (833, 'guest', '127.0.0.1', '内网IP', 'Chrome 143.0.0', 'Windows 10', '0', '登录成功', '2026-01-01 08:54:20', '', '2026-01-01 08:54:19', '', '2026-01-01 08:54:19', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for sys_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_menu`;
CREATE TABLE `sys_menu`  (
  `menu_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '菜单ID',
  `menu_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '菜单名称',
  `parent_id` int(11) NULL DEFAULT NULL COMMENT '父菜单ID',
  `order_num` float NULL DEFAULT NULL COMMENT '排序值',
  `path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '路由地址',
  `component` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '组件路径',
  `query` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '路由参数',
  `route_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '路由名称',
  `is_frame` int(11) NULL DEFAULT NULL COMMENT '是否为外链（0是 1否）',
  `is_cache` int(11) NULL DEFAULT NULL COMMENT '是否缓存（0缓存 1不缓存）',
  `menu_type` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单类型（M目录 C菜单 F按钮）',
  `visible` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单状态（0显示 1隐藏）',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单状态（0正常 1停用）',
  `perms` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '权限标识',
  `icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '菜单图标',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`menu_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1268 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_menu
-- ----------------------------
INSERT INTO `sys_menu` VALUES (1, '系统管理', 0, 1.99, 'system', NULL, '', '', 1, 0, 'M', '0', '0', '', 'system', 'admin', '2025-07-02 16:37:31', 'admin', '2025-08-01 23:30:57', '系统管理目录', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (2, '系统监控', 0, 2, 'monitor', NULL, '', '', 1, 0, 'M', '0', '0', '', 'monitor', 'admin', '2025-07-02 16:37:31', '', NULL, '系统监控目录', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (3, '系统工具', 0, 3, 'tool', NULL, '', '', 1, 0, 'M', '0', '0', '', 'tool', 'admin', '2025-07-02 16:37:31', '', NULL, '系统工具目录', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (4, 'CaseGo官网', 0, 4, 'http://8.130.23.175:88/', NULL, '', '', 0, 0, 'M', '0', '0', '', 'guide', 'admin', '2025-07-02 16:37:31', 'admin', '2025-12-31 14:43:49', '若依官网地址', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (100, '用户管理', 1, 1, 'user', 'system/user/index', '', '', 1, 0, 'C', '0', '0', 'system:user:list', 'user', 'admin', '2025-07-02 16:37:31', '', NULL, '用户管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (101, '角色管理', 1, 2, 'role', 'system/role/index', '', '', 1, 0, 'C', '0', '0', 'system:role:list', 'peoples', 'admin', '2025-07-02 16:37:31', '', NULL, '角色管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (102, '菜单管理', 1, 3, 'menu', 'system/menu/index', '', '', 1, 0, 'C', '0', '0', 'system:menu:list', 'tree-table', 'admin', '2025-07-02 16:37:31', '', NULL, '菜单管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (103, '部门管理', 1, 4, 'dept', 'system/dept/index', '', '', 1, 0, 'C', '0', '0', 'system:dept:list', 'tree', 'admin', '2025-07-02 16:37:31', '', NULL, '部门管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (104, '岗位管理', 1, 5, 'post', 'system/post/index', '', '', 1, 0, 'C', '0', '0', 'system:post:list', 'post', 'admin', '2025-07-02 16:37:31', '', NULL, '岗位管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (105, '字典管理', 1, 6, 'dict', 'system/dict/index', '', '', 1, 0, 'C', '0', '0', 'system:dict:list', 'dict', 'admin', '2025-07-02 16:37:31', '', NULL, '字典管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (106, '参数设置', 1, 7, 'config', 'system/config/index', '', '', 1, 0, 'C', '0', '0', 'system:config:list', 'edit', 'admin', '2025-07-02 16:37:31', '', NULL, '参数设置菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (107, '通知公告', 1, 8, 'notice', 'system/notice/index', '', '', 1, 0, 'C', '0', '0', 'system:notice:list', 'message', 'admin', '2025-07-02 16:37:31', '', NULL, '通知公告菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (108, '日志管理', 1, 9, 'log', '', '', '', 1, 0, 'M', '0', '0', '', 'log', 'admin', '2025-07-02 16:37:31', '', NULL, '日志管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (109, '在线用户', 2, 1, 'online', 'monitor/online/index', '', '', 1, 0, 'C', '0', '0', 'monitor:online:list', 'online', 'admin', '2025-07-02 16:37:31', '', NULL, '在线用户菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (110, '定时任务', 2, 2, 'job', 'monitor/job/index', '', '', 1, 0, 'C', '0', '0', 'monitor:job:list', 'job', 'admin', '2025-07-02 16:37:31', '', NULL, '定时任务菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (111, '数据监控', 2, 3, 'druid', 'monitor/druid/index', '', '', 1, 0, 'C', '0', '0', 'monitor:druid:list', 'druid', 'admin', '2025-07-02 16:37:31', '', NULL, '数据监控菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (112, '服务监控', 2, 4, 'server', 'monitor/server/index', '', '', 1, 0, 'C', '0', '0', 'monitor:server:list', 'server', 'admin', '2025-07-02 16:37:31', '', NULL, '服务监控菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (113, '缓存监控', 2, 5, 'cache', 'monitor/cache/index', '', '', 1, 0, 'C', '0', '0', 'monitor:cache:list', 'redis', 'admin', '2025-07-02 16:37:31', '', NULL, '缓存监控菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (114, '缓存列表', 2, 6, 'cacheList', 'monitor/cache/list', '', '', 1, 0, 'C', '0', '0', 'monitor:cache:list', 'redis-list', 'admin', '2025-07-02 16:37:31', '', NULL, '缓存列表菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (115, '表单构建', 3, 1, 'build', 'tool/build/index', '', '', 1, 0, 'C', '0', '0', 'tool:build:list', 'build', 'admin', '2025-07-02 16:37:31', '', NULL, '表单构建菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (116, '代码生成', 3, 2, 'gen', 'tool/gen/index', '', '', 1, 0, 'C', '0', '0', 'tool:gen:list', 'code', 'admin', '2025-07-02 16:37:31', '', NULL, '代码生成菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (117, '系统接口', 3, 3, 'swagger', 'tool/swagger/index', '', '', 1, 0, 'C', '0', '0', 'tool:swagger:list', 'swagger', 'admin', '2025-07-02 16:37:31', '', NULL, '系统接口菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (500, '操作日志', 108, 1, 'operlog', 'monitor/operlog/index', '', '', 1, 0, 'C', '0', '0', 'monitor:operlog:list', 'form', 'admin', '2025-07-02 16:37:31', '', NULL, '操作日志菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (501, '登录日志', 108, 2, 'logininfor', 'monitor/logininfor/index', '', '', 1, 0, 'C', '0', '0', 'monitor:logininfor:list', 'logininfor', 'admin', '2025-07-02 16:37:31', '', NULL, '登录日志菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1000, '用户查询', 100, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1001, '用户新增', 100, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1002, '用户修改', 100, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1003, '用户删除', 100, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1004, '用户导出', 100, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1005, '用户导入', 100, 6, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:import', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1006, '重置密码', 100, 7, '', '', '', '', 1, 0, 'F', '0', '0', 'system:user:resetPwd', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1007, '角色查询', 101, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1008, '角色新增', 101, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1009, '角色修改', 101, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1010, '角色删除', 101, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1011, '角色导出', 101, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:role:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1012, '菜单查询', 102, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1013, '菜单新增', 102, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1014, '菜单修改', 102, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1015, '菜单删除', 102, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:menu:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1016, '部门查询', 103, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1017, '部门新增', 103, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1018, '部门修改', 103, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1019, '部门删除', 103, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:dept:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1020, '岗位查询', 104, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1021, '岗位新增', 104, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1022, '岗位修改', 104, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1023, '岗位删除', 104, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1024, '岗位导出', 104, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'system:post:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1025, '字典查询', 105, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1026, '字典新增', 105, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1027, '字典修改', 105, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1028, '字典删除', 105, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1029, '字典导出', 105, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:dict:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1030, '参数查询', 106, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1031, '参数新增', 106, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1032, '参数修改', 106, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1033, '参数删除', 106, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1034, '参数导出', 106, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:config:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1035, '公告查询', 107, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1036, '公告新增', 107, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1037, '公告修改', 107, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1038, '公告删除', 107, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'system:notice:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1039, '操作查询', 500, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1040, '操作删除', 500, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1041, '日志导出', 500, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:operlog:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1042, '登录查询', 501, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1043, '登录删除', 501, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1044, '日志导出', 501, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1045, '账户解锁', 501, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:logininfor:unlock', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1046, '在线查询', 109, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1047, '批量强退', 109, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:batchLogout', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1048, '单条强退', 109, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:online:forceLogout', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1049, '任务查询', 110, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1050, '任务新增', 110, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:add', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1051, '任务修改', 110, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1052, '任务删除', 110, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1053, '状态修改', 110, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:changeStatus', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1054, '任务导出', 110, 6, '#', '', '', '', 1, 0, 'F', '0', '0', 'monitor:job:export', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1055, '生成查询', 116, 1, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:query', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1056, '生成修改', 116, 2, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:edit', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1057, '生成删除', 116, 3, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:remove', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1058, '导入代码', 116, 4, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:import', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1059, '预览代码', 116, 5, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:preview', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1060, '生成代码', 116, 6, '#', '', '', '', 1, 0, 'F', '0', '0', 'tool:gen:code', '#', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1061, '项目环境', 0, 1, 'project', NULL, NULL, '', 1, 0, 'M', '0', '0', NULL, 'server', 'admin', '2025-07-02 20:50:44', 'admin', '2025-12-03 20:45:43', '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1072, '数据库配置', 1061, 1, 'api_databases', 'api_databases/api_databases/index', NULL, NULL, 1, 0, 'C', '0', '0', 'api_databases:api_databases:list', 'redis', 'admin', '2025-07-30 17:39:28', 'admin', '2025-07-31 11:10:13', '数据库配置菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1073, '数据库配置查询', 1072, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_databases:api_databases:query', '#', 'admin', '2025-07-30 17:39:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1074, '数据库配置新增', 1072, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_databases:api_databases:add', '#', 'admin', '2025-07-30 17:39:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1075, '数据库配置修改', 1072, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_databases:api_databases:edit', '#', 'admin', '2025-07-30 17:39:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1076, '数据库配置删除', 1072, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_databases:api_databases:remove', '#', 'admin', '2025-07-30 17:39:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1077, '数据库配置导出', 1072, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_databases:api_databases:export', '#', 'admin', '2025-07-30 17:39:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1078, '环境配置', 1061, 1, 'environments', 'api_environments/environments/index', NULL, NULL, 1, 0, 'C', '0', '0', 'api_environments:environments:list', 'swagger', 'admin', '2025-07-30 23:19:47', 'admin', '2025-07-31 11:10:22', '环境配置菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1079, '环境配置查询', 1078, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_environments:environments:query', '#', 'admin', '2025-07-30 23:19:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1080, '环境配置新增', 1078, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_environments:environments:add', '#', 'admin', '2025-07-30 23:19:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1081, '环境配置修改', 1078, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_environments:environments:edit', '#', 'admin', '2025-07-30 23:19:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1082, '环境配置删除', 1078, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_environments:environments:remove', '#', 'admin', '2025-07-30 23:19:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1083, '环境配置导出', 1078, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_environments:environments:export', '#', 'admin', '2025-07-30 23:19:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1096, '项目管理', 1061, 0, 'project', 'api_project/project/index', NULL, NULL, 1, 0, 'C', '0', '0', 'api_project:project:list', 'server', 'admin', '2025-08-01 09:17:09', 'admin', '2025-08-02 20:24:31', '项目菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1097, '项目查询', 1096, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project:project:query', '#', 'admin', '2025-08-01 09:17:09', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1098, '项目新增', 1096, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project:project:add', '#', 'admin', '2025-08-01 09:17:09', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1099, '项目修改', 1096, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project:project:edit', '#', 'admin', '2025-08-01 09:17:09', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1100, '项目删除', 1096, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project:project:remove', '#', 'admin', '2025-08-01 09:17:09', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1101, '项目导出', 1096, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project:project:export', '#', 'admin', '2025-08-01 09:17:09', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1108, '环境服务地址', 1061, 1, 'services', 'api_services/services/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_services:services:list', '404', 'admin', '2025-08-01 15:34:57', 'admin', '2025-12-15 09:58:44', '环境服务地址菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1109, '环境服务地址查询', 1108, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:query', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1110, '环境服务地址新增', 1108, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:add', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1111, '环境服务地址修改', 1108, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:edit', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1112, '环境服务地址删除', 1108, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:remove', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1113, '环境服务地址导出', 1108, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:export', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1114, '接口测试', 0, 1.5, 'api-management', NULL, NULL, '', 1, 0, 'M', '0', '0', NULL, '组件API管理', 'admin', '2025-08-01 21:49:17', 'admin', '2025-12-24 16:53:24', '', NULL, NULL, 0);
INSERT INTO `sys_menu` VALUES (1115, '环境缓存', 1061, 1, 'cache_data', 'api_cache_data/cache_data/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_cache_data:cache_data:list', '404', 'admin', '2025-08-02 00:44:01', 'admin', '2025-12-15 09:58:52', '环境缓存菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1116, '环境缓存查询', 1115, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:query', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1117, '环境缓存新增', 1115, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:add', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1118, '环境缓存修改', 1115, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:edit', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1119, '环境缓存删除', 1115, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:remove', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1120, '环境缓存导出', 1115, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:export', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1121, '环境服务地址查询', 1078, 6, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:query', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1122, '环境服务地址新增', 1078, 7, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:add', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1123, '环境服务地址修改', 1078, 8, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:edit', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1124, '环境服务地址删除', 1078, 9, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:remove', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1125, '环境服务地址导出', 1078, 10, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:export', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1126, '环境服务地址列表', 1078, 11, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_services:services:list', '#', 'admin', '2025-08-01 15:34:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1127, '环境缓存查询', 1078, 11, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:query', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1128, '环境缓存新增', 1078, 12, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:add', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1129, '环境缓存修改', 1078, 13, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:edit', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1130, '环境缓存删除', 1078, 14, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:remove', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1131, '环境缓存导出', 1078, 15, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:export', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1132, '环境缓存列表', 1078, 16, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cache_data:cache_data:list', '#', 'admin', '2025-08-02 00:44:01', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1139, '项目模块', 1061, 1, 'project_submodules', 'api_project_submodules/project_submodules/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_project_submodules:project_submodules:list', '#', 'admin', '2025-08-03 13:57:42', 'admin', '2025-08-05 17:17:45', '项目模块菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1140, '项目模块查询', 1139, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project_submodules:project_submodules:query', '#', 'admin', '2025-08-03 13:57:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1141, '项目模块新增', 1139, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project_submodules:project_submodules:add', '#', 'admin', '2025-08-03 13:57:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1142, '项目模块修改', 1139, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project_submodules:project_submodules:edit', '#', 'admin', '2025-08-03 13:57:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1143, '项目模块删除', 1139, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project_submodules:project_submodules:remove', '#', 'admin', '2025-08-03 13:57:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1144, '项目模块导出', 1139, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_project_submodules:project_submodules:export', '#', 'admin', '2025-08-03 13:57:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1151, '接口用例', 1114, 0.5, 'test_cases', 'api_test_cases/test_cases/index', NULL, NULL, 1, 0, 'C', '0', '0', 'api_test_cases:test_cases:list', 'API用例', 'admin', '2025-08-03 22:11:17', 'admin', '2025-12-24 16:42:55', '接口用例菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1152, '接口用例查询', 1151, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_cases:test_cases:query', '#', 'admin', '2025-08-03 22:11:17', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1153, '接口用例新增', 1151, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_cases:test_cases:add', '#', 'admin', '2025-08-03 22:11:17', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1154, '接口用例修改', 1151, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_cases:test_cases:edit', '#', 'admin', '2025-08-03 22:11:17', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1155, '接口用例删除', 1151, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_cases:test_cases:remove', '#', 'admin', '2025-08-03 22:11:17', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1156, '接口用例导出', 1151, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_cases:test_cases:export', '#', 'admin', '2025-08-03 22:11:17', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1157, 'workflows', 1114, 1, 'workflows', 'api_workflow/components/workflow/WorkflowDesigner', NULL, NULL, 1, 0, 'C', '1', '0', 'api_cookies:cookies:list', '#', 'admin', '2025-08-03 22:12:56', 'admin', '2025-12-12 10:31:17', '接口请求Cookie菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1158, '接口请求Cookie查询', 1157, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cookies:cookies:query', '#', 'admin', '2025-08-03 22:12:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1159, '接口请求Cookie新增', 1157, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cookies:cookies:add', '#', 'admin', '2025-08-03 22:12:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1160, '接口请求Cookie修改', 1157, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cookies:cookies:edit', '#', 'admin', '2025-08-03 22:12:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1161, '接口请求Cookie删除', 1157, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cookies:cookies:remove', '#', 'admin', '2025-08-03 22:12:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1162, '接口请求Cookie导出', 1157, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_cookies:cookies:export', '#', 'admin', '2025-08-03 22:12:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1163, '接口请求头', 1114, 1, 'headers', 'api_headers/headers/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_headers:headers:list', '#', 'admin', '2025-08-03 22:13:28', 'admin', '2025-12-12 10:32:38', '接口请求头菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1164, '接口请求头查询', 1163, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_headers:headers:query', '#', 'admin', '2025-08-03 22:13:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1165, '接口请求头新增', 1163, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_headers:headers:add', '#', 'admin', '2025-08-03 22:13:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1166, '接口请求头修改', 1163, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_headers:headers:edit', '#', 'admin', '2025-08-03 22:13:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1167, '接口请求头删除', 1163, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_headers:headers:remove', '#', 'admin', '2025-08-03 22:13:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1168, '接口请求头导出', 1163, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_headers:headers:export', '#', 'admin', '2025-08-03 22:13:28', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1169, '接口请求参数', 1114, 1, 'params', 'api_params/params/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_params:params:list', '#', 'admin', '2025-08-03 22:13:42', 'admin', '2025-12-12 10:31:31', '接口请求参数菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1170, '接口请求参数查询', 1169, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_params:params:query', '#', 'admin', '2025-08-03 22:13:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1171, '接口请求参数新增', 1169, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_params:params:add', '#', 'admin', '2025-08-03 22:13:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1172, '接口请求参数修改', 1169, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_params:params:edit', '#', 'admin', '2025-08-03 22:13:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1173, '接口请求参数删除', 1169, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_params:params:remove', '#', 'admin', '2025-08-03 22:13:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1174, '接口请求参数导出', 1169, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_params:params:export', '#', 'admin', '2025-08-03 22:13:42', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1175, '接口前置操作', 1114, 1, 'setup', 'api_setup/setup/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_setup:setup:list', '#', 'admin', '2025-08-03 22:13:57', 'admin', '2025-12-12 10:31:37', '接口前置操作菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1176, '接口前置操作查询', 1175, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_setup:setup:query', '#', 'admin', '2025-08-03 22:13:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1177, '接口前置操作新增', 1175, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_setup:setup:add', '#', 'admin', '2025-08-03 22:13:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1178, '接口前置操作修改', 1175, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_setup:setup:edit', '#', 'admin', '2025-08-03 22:13:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1179, '接口前置操作删除', 1175, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_setup:setup:remove', '#', 'admin', '2025-08-03 22:13:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1180, '接口前置操作导出', 1175, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_setup:setup:export', '#', 'admin', '2025-08-03 22:13:57', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1181, '接口后置操作', 1114, 1, 'teardown', 'api_teardown/teardown/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_teardown:teardown:list', '#', 'admin', '2025-08-03 22:14:14', 'admin', '2025-12-12 10:32:43', '接口后置操作菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1182, '接口后置操作查询', 1181, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_teardown:teardown:query', '#', 'admin', '2025-08-03 22:14:14', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1183, '接口后置操作新增', 1181, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_teardown:teardown:add', '#', 'admin', '2025-08-03 22:14:14', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1184, '接口后置操作修改', 1181, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_teardown:teardown:edit', '#', 'admin', '2025-08-03 22:14:14', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1185, '接口后置操作删除', 1181, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_teardown:teardown:remove', '#', 'admin', '2025-08-03 22:14:14', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1186, '接口后置操作导出', 1181, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_teardown:teardown:export', '#', 'admin', '2025-08-03 22:14:14', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1187, '接口断言', 1114, 1, 'assertions', 'api_assertions/assertions/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_assertions:assertions:list', '#', 'admin', '2025-08-04 15:15:45', 'admin', '2025-12-12 10:31:42', '接口断言菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1188, '接口断言查询', 1187, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_assertions:assertions:query', '#', 'admin', '2025-08-04 15:15:45', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1189, '接口断言新增', 1187, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_assertions:assertions:add', '#', 'admin', '2025-08-04 15:15:45', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1190, '接口断言修改', 1187, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_assertions:assertions:edit', '#', 'admin', '2025-08-04 15:15:45', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1191, '接口断言删除', 1187, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_assertions:assertions:remove', '#', 'admin', '2025-08-04 15:15:45', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1192, '接口断言导出', 1187, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_assertions:assertions:export', '#', 'admin', '2025-08-04 15:15:45', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1193, '接口单body', 1114, 1, 'formdata', 'api_formdata/formdata/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_formdata:formdata:list', '#', 'admin', '2025-08-06 17:43:59', 'admin', '2025-12-12 10:31:47', '接口单body菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1194, '接口单body查询', 1193, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_formdata:formdata:query', '#', 'admin', '2025-08-06 17:43:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1195, '接口单body新增', 1193, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_formdata:formdata:add', '#', 'admin', '2025-08-06 17:43:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1196, '接口单body修改', 1193, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_formdata:formdata:edit', '#', 'admin', '2025-08-06 17:43:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1197, '接口单body删除', 1193, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_formdata:formdata:remove', '#', 'admin', '2025-08-06 17:43:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1198, '接口单body导出', 1193, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_formdata:formdata:export', '#', 'admin', '2025-08-06 17:43:59', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1199, '附件管理', 1, 1, 'file', 'system/file/index', NULL, NULL, 1, 0, 'C', '0', '0', 'system:file:list', 'documentation', 'admin', '2025-08-22 15:12:05', 'admin', '2025-08-22 15:28:09', '附件管理菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1200, '附件管理查询', 1199, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'system:file:query', '#', 'admin', '2025-08-22 15:12:05', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1201, '附件管理新增', 1199, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'system:file:add', '#', 'admin', '2025-08-22 15:12:05', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1202, '附件管理修改', 1199, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'system:file:edit', '#', 'admin', '2025-08-22 15:12:05', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1203, '附件管理删除', 1199, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'system:file:remove', '#', 'admin', '2025-08-22 15:12:05', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1204, '附件管理导出', 1199, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'system:file:export', '#', 'admin', '2025-08-22 15:12:05', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1205, '自动化测试', 1114, 0.6, 'workflow', 'api_workflow/index', NULL, NULL, 1, 0, 'C', '0', '0', 'workflow:workflow:list', '自动化测试', 'admin', '2025-08-28 15:18:53', 'admin', '2025-12-24 16:44:22', '测试执行器主菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1206, '测试执行器主查询', 1205, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'workflow:workflow:query', '#', 'admin', '2025-08-28 15:18:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1207, '测试执行器主新增', 1205, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'workflow:workflow:add', '#', 'admin', '2025-08-28 15:18:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1208, '测试执行器主修改', 1205, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'workflow:workflow:edit', '#', 'admin', '2025-08-28 15:18:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1209, '测试执行器主删除', 1205, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'workflow:workflow:remove', '#', 'admin', '2025-08-28 15:18:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1210, '测试执行器主导出', 1205, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'workflow:workflow:export', '#', 'admin', '2025-08-28 15:18:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1211, '执行器执行记录', 1114, 1, 'workflow_executions', 'api_workflow_executions/workflow_executions/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_workflow_executions:workflow_executions:list', '#', 'admin', '2025-08-28 15:55:29', 'admin', '2025-12-12 10:31:53', '执行器执行记录菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1212, '执行器执行记录查询', 1211, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_workflow_executions:workflow_executions:query', '#', 'admin', '2025-08-28 15:55:29', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1213, '执行器执行记录新增', 1211, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_workflow_executions:workflow_executions:add', '#', 'admin', '2025-08-28 15:55:29', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1214, '执行器执行记录修改', 1211, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_workflow_executions:workflow_executions:edit', '#', 'admin', '2025-08-28 15:55:29', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1215, '执行器执行记录删除', 1211, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_workflow_executions:workflow_executions:remove', '#', 'admin', '2025-08-28 15:55:29', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1216, '执行器执行记录导出', 1211, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_workflow_executions:workflow_executions:export', '#', 'admin', '2025-08-28 15:55:29', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1217, '节点执行记录', 1114, 1, 'worknode_executions', 'api_worknode_executions/worknode_executions/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_worknode_executions:worknode_executions:list', '#', 'admin', '2025-08-28 16:21:24', 'admin', '2025-12-12 10:32:00', '节点执行记录菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1218, '节点执行记录查询', 1217, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknode_executions:worknode_executions:query', '#', 'admin', '2025-08-28 16:21:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1219, '节点执行记录新增', 1217, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknode_executions:worknode_executions:add', '#', 'admin', '2025-08-28 16:21:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1220, '节点执行记录修改', 1217, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknode_executions:worknode_executions:edit', '#', 'admin', '2025-08-28 16:21:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1221, '节点执行记录删除', 1217, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknode_executions:worknode_executions:remove', '#', 'admin', '2025-08-28 16:21:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1222, '节点执行记录导出', 1217, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknode_executions:worknode_executions:export', '#', 'admin', '2025-08-28 16:21:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1223, '执行器节点', 1114, 1, 'worknodes', 'api_worknodes/worknodes/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_worknodes:worknodes:list', '#', 'admin', '2025-08-28 16:31:25', 'admin', '2025-12-12 10:32:51', '执行器节点菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1224, '执行器节点查询', 1223, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknodes:worknodes:query', '#', 'admin', '2025-08-28 16:31:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1225, '执行器节点新增', 1223, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknodes:worknodes:add', '#', 'admin', '2025-08-28 16:31:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1226, '执行器节点修改', 1223, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknodes:worknodes:edit', '#', 'admin', '2025-08-28 16:31:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1227, '执行器节点删除', 1223, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknodes:worknodes:remove', '#', 'admin', '2025-08-28 16:31:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1228, '执行器节点导出', 1223, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_worknodes:worknodes:export', '#', 'admin', '2025-08-28 16:31:25', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1229, '接口测试执行日志', 1114, 1, 'execution_log', 'api_test_execution_log/execution_log/index', NULL, NULL, 1, 0, 'C', '1', '0', 'api_test_execution_log:execution_log:list', '#', 'admin', '2025-11-02 22:49:56', 'admin', '2025-11-03 14:00:44', '接口测试执行日志菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1230, '接口测试执行日志查询', 1229, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_execution_log:execution_log:query', '#', 'admin', '2025-11-02 22:49:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1231, '接口测试执行日志新增', 1229, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_execution_log:execution_log:add', '#', 'admin', '2025-11-02 22:49:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1232, '接口测试执行日志修改', 1229, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_execution_log:execution_log:edit', '#', 'admin', '2025-11-02 22:49:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1233, '接口测试执行日志删除', 1229, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_execution_log:execution_log:remove', '#', 'admin', '2025-11-02 22:49:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1234, '接口测试执行日志导出', 1229, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_test_execution_log:execution_log:export', '#', 'admin', '2025-11-02 22:49:56', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1235, '参数化数据行', 1114, 1, 'api_param_item', 'item/api_param_item/index', NULL, NULL, 1, 0, 'C', '1', '0', 'item:api_param_item:list', '#', 'admin', '2025-11-13 22:45:19', 'admin', '2025-12-12 10:32:04', '参数化数据行菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1236, '参数化数据行查询', 1235, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'item:api_param_item:query', '#', 'admin', '2025-11-13 22:45:19', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1237, '参数化数据行新增', 1235, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'item:api_param_item:add', '#', 'admin', '2025-11-13 22:45:19', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1238, '参数化数据行修改', 1235, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'item:api_param_item:edit', '#', 'admin', '2025-11-13 22:45:19', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1239, '参数化数据行删除', 1235, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'item:api_param_item:remove', '#', 'admin', '2025-11-13 22:45:19', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1240, '参数化数据行导出', 1235, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'item:api_param_item:export', '#', 'admin', '2025-11-13 22:45:19', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1241, '参数化数据主', 1114, 1, 'api_param_table', 'table/api_param_table/index', NULL, NULL, 1, 0, 'C', '1', '0', 'table:api_param_table:list', '#', 'admin', '2025-11-13 22:45:52', 'admin', '2025-12-12 10:32:08', '参数化数据主菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1242, '参数化数据主查询', 1241, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'table:api_param_table:query', '#', 'admin', '2025-11-13 22:45:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1243, '参数化数据主新增', 1241, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'table:api_param_table:add', '#', 'admin', '2025-11-13 22:45:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1244, '参数化数据主修改', 1241, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'table:api_param_table:edit', '#', 'admin', '2025-11-13 22:45:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1245, '参数化数据主删除', 1241, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'table:api_param_table:remove', '#', 'admin', '2025-11-13 22:45:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1246, '参数化数据主导出', 1241, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'table:api_param_table:export', '#', 'admin', '2025-11-13 22:45:53', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1248, '自动化测试执行报告', 1114, 1, 'api_workflow_report', 'report/api_workflow_report/index', NULL, NULL, 1, 0, 'C', '1', '0', 'report:api_workflow_report:list', '#', 'admin', '2025-11-30 18:09:24', 'admin', '2025-12-12 10:32:12', '自动化测试执行报告菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1249, '自动化测试执行报告查询', 1248, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'report:api_workflow_report:query', '#', 'admin', '2025-11-30 18:09:24', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1250, '自动化测试执行报告新增', 1248, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'report:api_workflow_report:add', '#', 'admin', '2025-11-30 18:09:24', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1251, '自动化测试执行报告修改', 1248, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'report:api_workflow_report:edit', '#', 'admin', '2025-11-30 18:09:24', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1252, '自动化测试执行报告删除', 1248, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'report:api_workflow_report:remove', '#', 'admin', '2025-11-30 18:09:24', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1253, '自动化测试执行报告导出', 1248, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'report:api_workflow_report:export', '#', 'admin', '2025-11-30 18:09:24', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1254, '通知消息', 1114, 1, 'notification', 'task_notification/notification/index', NULL, NULL, 1, 0, 'C', '0', '0', 'task_notification:notification:list', 'message', 'admin', '2025-12-03 20:51:38', 'admin', '2025-12-24 16:44:45', '通知消息菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1255, '通知消息查询', 1254, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'task_notification:notification:query', '#', 'admin', '2025-12-03 20:51:38', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1256, '通知消息新增', 1254, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'task_notification:notification:add', '#', 'admin', '2025-12-03 20:51:38', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1257, '通知消息修改', 1254, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'task_notification:notification:edit', '#', 'admin', '2025-12-03 20:51:38', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1258, '通知消息删除', 1254, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'task_notification:notification:remove', '#', 'admin', '2025-12-03 20:51:38', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1259, '通知消息导出', 1254, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'task_notification:notification:export', '#', 'admin', '2025-12-03 20:51:38', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1260, '公共脚本库', 1266, 1, 'script_library', 'api_script_library/script_library/index', NULL, NULL, 1, 0, 'C', '0', '0', 'api_script_library:script_library:list', 'python脚本30_30', 'admin', '2025-12-13 17:54:20', 'admin', '2025-12-24 16:46:50', '公共脚本库菜单', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1261, '公共脚本库查询', 1260, 1, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_script_library:script_library:query', '#', 'admin', '2025-12-13 17:54:20', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1262, '公共脚本库新增', 1260, 2, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_script_library:script_library:add', '#', 'admin', '2025-12-13 17:54:20', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1263, '公共脚本库修改', 1260, 3, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_script_library:script_library:edit', '#', 'admin', '2025-12-13 17:54:20', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1264, '公共脚本库删除', 1260, 4, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_script_library:script_library:remove', '#', 'admin', '2025-12-13 17:54:20', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1265, '公共脚本库导出', 1260, 5, '#', '', NULL, NULL, 1, 0, 'F', '0', '0', 'api_script_library:script_library:export', '#', 'admin', '2025-12-13 17:54:20', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_menu` VALUES (1266, '工具', 0, 1.6, 'utils', NULL, NULL, '', 1, 0, 'M', '0', '0', NULL, '工具箱,辅助工具_jurassic', 'admin', '2025-12-15 03:18:53', 'admin', '2025-12-24 16:39:41', NULL, NULL, 1, 0);
INSERT INTO `sys_menu` VALUES (1267, '自定义函数', 1266, 1, 'faker-func', 'utils/index', NULL, 'faker-func', 1, 0, 'C', '0', '0', NULL, '函数-计算函数', 'admin', '2025-12-15 03:24:40', 'admin', '2025-12-24 16:48:09', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for sys_notice
-- ----------------------------
DROP TABLE IF EXISTS `sys_notice`;
CREATE TABLE `sys_notice`  (
  `notice_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '公告ID',
  `notice_title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告标题',
  `notice_type` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告类型（1通知 2公告）',
  `notice_content` blob NULL COMMENT '公告内容',
  `status` char(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '公告状态（0正常 1关闭）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`notice_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_notice
-- ----------------------------
INSERT INTO `sys_notice` VALUES (1, '温馨提醒：2018-07-01 casego新版本发布啦', '2', 0xE696B0E78988E69CACE58685E5AEB9, '0', 'admin', '2025-07-02 16:37:33', '', NULL, '管理员', NULL, NULL, NULL);
INSERT INTO `sys_notice` VALUES (2, '维护通知：2018-07-01 casego系统凌晨维护', '1', 0xE7BBB4E68AA4E58685E5AEB9, '0', 'admin', '2025-07-02 16:37:33', '', NULL, '管理员', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for sys_oper_log
-- ----------------------------
DROP TABLE IF EXISTS `sys_oper_log`;
CREATE TABLE `sys_oper_log`  (
  `oper_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '日志主键',
  `title` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '模块标题',
  `business_type` int(11) NULL DEFAULT NULL COMMENT '业务类型（0其它 1新增 2修改 3删除）',
  `method` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '方法名称',
  `request_method` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '请求方式',
  `operator_type` int(11) NULL DEFAULT NULL COMMENT '操作类别（0其它 1后台用户 2手机端用户）',
  `oper_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作人员',
  `dept_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '部门名称',
  `oper_url` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求URL',
  `oper_ip` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '主机地址',
  `oper_location` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '操作地点',
  `oper_param` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '请求参数',
  `json_result` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '返回参数',
  `status` int(11) NULL DEFAULT NULL COMMENT '操作状态（0正常 1异常）',
  `error_msg` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '错误消息',
  `oper_time` datetime NULL DEFAULT NULL COMMENT '操作时间',
  `cost_time` bigint(20) NULL DEFAULT NULL COMMENT '消耗时间',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`oper_id`) USING BTREE,
  INDEX `idx_sys_oper_log_bt`(`business_type`) USING BTREE,
  INDEX `idx_sys_oper_log_ot`(`oper_time`) USING BTREE,
  INDEX `idx_sys_oper_log_s`(`status`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2066 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_oper_log
-- ----------------------------

-- ----------------------------
-- Table structure for sys_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_post`;
CREATE TABLE `sys_post`  (
  `post_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '岗位ID',
  `post_code` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '岗位编码',
  `post_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '岗位名称',
  `post_sort` int(11) NOT NULL COMMENT '显示顺序',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`post_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_post
-- ----------------------------
INSERT INTO `sys_post` VALUES (1, 'ceo', '董事长', 1, '0', 'admin', '2025-07-02 16:37:31', 'admin', '2025-07-08 10:29:07', '', NULL, NULL, NULL);
INSERT INTO `sys_post` VALUES (2, 'se', '项目经理', 2, '0', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_post` VALUES (3, 'hr', '人力资源', 3, '0', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);
INSERT INTO `sys_post` VALUES (4, 'user', '普通员工', 4, '0', 'admin', '2025-07-02 16:37:31', '', NULL, '', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for sys_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_role`;
CREATE TABLE `sys_role`  (
  `role_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '角色ID',
  `role_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色名称',
  `role_key` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色权限字符串',
  `role_sort` int(11) NOT NULL COMMENT '显示顺序',
  `data_scope` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据范围（1：全部数据权限 2：自定数据权限 3：本部门数据权限 4：本部门及以下数据权限）',
  `menu_check_strictly` int(11) NULL DEFAULT NULL COMMENT '菜单树选择项是否关联显示',
  `dept_check_strictly` int(11) NULL DEFAULT NULL COMMENT '部门树选择项是否关联显示',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '角色状态（0正常 1停用）',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`role_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role
-- ----------------------------
INSERT INTO `sys_role` VALUES (1, '超级管理员', 'admin', 1, '1', 1, 1, '0', 'admin', '2025-07-02 16:37:31', '', NULL, '超级管理员', NULL, NULL, 0);
INSERT INTO `sys_role` VALUES (2, '演示环境限制删除', 'common', 2, '3', 0, 1, '0', 'admin', '2025-07-02 16:37:31', 'admin', '2025-12-30 11:37:50', '普通角色', NULL, NULL, 0);

-- ----------------------------
-- Table structure for sys_role_dept
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_dept`;
CREATE TABLE `sys_role_dept`  (
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `dept_id` bigint(20) NOT NULL COMMENT '部门ID',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`role_id`, `dept_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_dept
-- ----------------------------

-- ----------------------------
-- Table structure for sys_role_menu
-- ----------------------------
DROP TABLE IF EXISTS `sys_role_menu`;
CREATE TABLE `sys_role_menu`  (
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `menu_id` bigint(20) NOT NULL COMMENT '菜单ID',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`role_id`, `menu_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_role_menu
-- ----------------------------
INSERT INTO `sys_role_menu` VALUES (2, 115, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 3, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 114, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 113, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1051, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1049, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 110, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1046, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 109, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 2, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1202, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1200, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1199, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1263, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1262, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1261, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1260, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1257, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1256, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1255, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1254, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1253, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1251, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1250, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1249, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1248, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1246, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1245, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1244, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1243, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1242, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1241, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1240, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1239, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1238, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1237, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1236, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1235, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1232, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1231, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1230, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1229, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1226, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1225, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1224, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1220, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1219, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1218, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1214, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1213, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1212, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1196, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1195, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1194, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1190, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1189, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1188, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1184, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1183, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1182, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1168, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1166, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1165, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1164, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1162, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1160, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1159, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1158, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1210, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1208, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1207, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1206, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1205, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1156, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1155, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1154, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1153, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1152, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1151, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1114, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1140, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1139, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1132, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1131, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1130, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1129, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1128, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1127, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1126, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1125, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1124, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1123, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1122, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1121, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1083, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1082, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1081, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1080, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1079, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1078, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1077, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1075, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1074, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1073, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1072, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1101, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1099, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1098, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1097, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1096, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 1061, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 117, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);
INSERT INTO `sys_role_menu` VALUES (2, 4, '', '2025-12-30 11:37:49', '', '2025-12-30 11:37:49', NULL, NULL, 1, 0);

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `dept_id` int(11) NULL DEFAULT NULL COMMENT '部门ID',
  `user_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户账号',
  `nick_name` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户昵称',
  `user_type` varchar(2) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户类型（00系统用户）',
  `email` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户邮箱',
  `phonenumber` varchar(11) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号码',
  `sex` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '用户性别（0男 1女 2未知）',
  `avatar` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '头像地址',
  `password` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '密码',
  `status` varchar(1) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '帐号状态（0正常 1停用）',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  `login_ip` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '最后登录IP',
  `login_date` datetime NULL DEFAULT NULL COMMENT '最后登录时间',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 80 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 103, 'admin', '超级管理员', '00', 'niangao@163.com', '15888888888', '1', '/profile/avatar/2025/12/29/avatar_20251229225234A864.png', '$2b$12$nGJyZD2lhbTdGkiEzUnQIOCa9HrInxZ42cZXy.2zeK7T4F.iR1Hp2', '0', 0, '127.0.0.1', '2026-01-01 08:51:57', 'admin', '2025-07-02 16:37:31', 'admin', '2025-12-31 14:46:33', '管理员', NULL, NULL);
INSERT INTO `sys_user` VALUES (2, 105, 'niangao', '年糕', '00', 'niangao@qq.com', '15666666666', '1', '', '$2a$10$7JB720yubVSZvUI0rEqK/.VqGOZTH.ulu33dHOiBE8ByOhJIrdAu2', '0', 0, '127.0.0.1', '2025-07-09 22:17:30', 'admin', '2025-07-02 16:37:31', 'admin', '2025-07-30 14:15:43', '测试员', NULL, NULL);
INSERT INTO `sys_user` VALUES (10, NULL, 'david', 'david', '00', '', '', '0', '', '$2b$12$JBt3hCmd9oyQQJLh1sVdU.n/vAsmoD3OS.YZtln7Ik0ClgwW3MECu', '0', 0, '', '2025-12-23 00:32:59', '', '2025-08-09 10:14:29', '', '2025-08-09 10:14:29', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (11, NULL, 'guest', 'guest', '00', '', '', '0', '/profile/avatar/2026/01/01/avatar_20260101085443A882.png', '$2b$12$8ybWOtqzEG6K51Brfq2Mm.aGdK0V00InDsFf1sEymcEziU1pfIkfS', '0', 0, '', '2026-01-01 08:54:20', '', '2025-08-10 18:47:47', 'guest', '2026-01-01 08:54:44', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (12, NULL, 'david2', 'david2', '00', '', '', '0', '', '$2b$12$WfhcQ40HA4EdDsekTIoghuypSVUvWSQXf1Gc/Z7nlQZCpXCgw0a6C', '0', 2, '', '2025-08-10 19:17:27', '', '2025-08-10 18:47:47', 'admin', '2025-12-18 22:03:04', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (13, NULL, 'david3', 'david3', '00', '', '', '0', '', '$2b$12$IRq6H.lh7D9BRwWNNHmTiO77KsydmmnOYpXDDL5v.foKOJYJYnLDS', '0', 2, '', '2025-08-10 19:24:18', '', '2025-08-10 18:47:47', 'admin', '2025-12-18 22:03:04', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (14, NULL, 'dawei', 'dawei', '00', '', '', '0', '', '$2b$12$20wsKAYVt5na8Gg8bFkjC.6TPx9ut4tw/Gdqivq40IJWbmPuCyBaS', '0', 2, '', '2025-10-31 16:28:52', '', '2025-10-31 10:53:39', 'admin', '2025-12-18 22:03:04', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (15, NULL, 'xiaxie', 'xiaxie', '00', '', '', '0', '', '$2b$12$m/e1O0zaDHBo1/bYlK.7FeJwl/twQkN9wFEQMJkPo82SH5Iskxwjq', '0', 2, '', NULL, '', '2025-12-18 14:47:31', 'admin', '2025-12-18 22:03:04', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (16, NULL, 'juanqiao', 'juanqiao', '00', '', '', '0', '', '$2b$12$QydmT8sJyDlEr4WPxxK6RuPuAQOpJpnkX/qM9SeIy0l1G1/59EadC', '0', 2, '', NULL, '', '2025-12-18 15:05:42', 'admin', '2025-12-18 22:03:04', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (17, NULL, 'xiuyingyu', 'xiuyingyu', '00', '', '', '0', '', '$2b$12$epjd/fJ5Q5Uxat80ZqPtYO7YN4OKUiO/C8.a6MPRki9zIZN8q3UOi', '0', 2, '', NULL, '', '2025-12-18 15:08:54', 'admin', '2025-12-18 22:03:04', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (18, NULL, 'qwen', 'qwen', '00', '', '', '0', '', '$2b$12$xQPd9BjWJ3P6iWiJL2o9LeLdKY7V7Qqhk0oYlKHU6LmNiIPKKVfK.', '0', 2, '', NULL, '', '2025-12-18 15:09:10', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (19, NULL, 'ctang', 'ctang', '00', '', '', '0', '', '$2b$12$Rixfy61/mrmgm0fBK2J22uicpc.EE/bSHo/TgMXmBJA8cWhUO0oli', '0', 2, '', NULL, '', '2025-12-18 15:09:12', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (20, NULL, 'fanglu', 'fanglu', '00', '', '', '0', '', '$2b$12$C4sLjFD4Ew1wzUZB5SCaie3KhFwJ4p/5SNRPVPpTYNKXuQOHGSQre', '0', 2, '', NULL, '', '2025-12-18 15:09:14', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (21, NULL, 'jdong', 'jdong', '00', '', '', '0', '', '$2b$12$8Ksxeopux14Nt019FUh6xud7m1iKzDKKSTI/0fVJYZQFCwSBciwcm', '0', 2, '', NULL, '', '2025-12-18 15:09:17', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (22, NULL, 'qfan', 'qfan', '00', '', '', '0', '', '$2b$12$IGZQmLIM.Nrzvt77a5iXUOaT4iTr4WgFxbkrfkfCsml/oZD0NIYIu', '0', 2, '', NULL, '', '2025-12-18 15:09:19', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (23, NULL, 'xmeng', 'xmeng', '00', '', '', '0', '', '$2b$12$RwGj566IeLpCkRWxfeXLhuc/vOTj95kvAopJs01vCH1lmnkyPiBCK', '0', 2, '', NULL, '', '2025-12-18 15:09:22', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (24, NULL, 'xuyong', 'xuyong', '00', '', '', '0', '', '$2b$12$5utBQK/oHkIK//ulgkh13OfjTTv/nvXHy1tL8pO8bk.bwSlSNu1IK', '0', 2, '', NULL, '', '2025-12-18 15:09:24', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (25, NULL, 'jiefan', 'jiefan', '00', '', '', '0', '', '$2b$12$mF9ZPBAu4RYaqUvSmq9WJODOMiZQNk2L0gyYq.Rw9CrrLZ80I2Gka', '0', 2, '', NULL, '', '2025-12-18 15:09:27', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (26, NULL, 'min77', 'min77', '00', '', '', '0', '', '$2b$12$rCK9NePZl.SxAqM78vOlsOZ7GNCvzcfGIseXpbhsQOpOxRS8wEzwS', '0', 2, '', NULL, '', '2025-12-18 15:09:29', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (27, NULL, 'fliang', 'fliang', '00', '', '', '0', '', '$2b$12$phpHiNWC8rtbOpRFpS/DZed8J9SS2d80IlOVjyC9aQ8Vmk8Y4P0lC', '0', 2, '', NULL, '', '2025-12-18 15:09:31', 'admin', '2025-12-18 22:02:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (28, NULL, 'changqiang', 'changqiang', '00', '', '', '0', '', '$2b$12$kWYKjyGmMcYaZQ/j6G/kFu8AiklQtKybx4bcVXDNbMPFhHaU46zsG', '0', 2, '', NULL, '', '2025-12-18 15:11:36', 'admin', '2025-12-18 22:02:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (29, NULL, 'igao', 'igao', '00', '', '', '0', '', '$2b$12$eY9vRTVqQ.mQlQxKWmeBH.B9e1V6EXFQExYMxJtvmRy8LVDv9tdJG', '0', 2, '', NULL, '', '2025-12-18 15:14:16', 'admin', '2025-12-18 22:02:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (30, NULL, 'taozeng', 'taozeng', '00', '', '', '0', '', '$2b$12$EKOot0UsETO/IpWvIN0nzeWlP8tWtGZ2SYCqxGaMnw5IrptfIS.TO', '0', 2, '', NULL, '', '2025-12-18 15:15:22', 'admin', '2025-12-18 22:02:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (31, NULL, 'huchao', 'huchao', '00', '', '', '0', '', '$2b$12$/Uvydb/VVu/mhjJRgDdDBuK0jym2..SnVDSL/BMi11P.xCjNwBGou', '0', 2, '', '2025-12-18 15:28:34', '', '2025-12-18 15:28:33', 'admin', '2025-12-18 22:02:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (32, NULL, 'lishen', 'lishen', '00', '', '', '0', '', '$2b$12$ShrgwuTraAdoxjWsnkP.2.DXjlJ9SfK6X/gcVlMktK8wFh59ec4uS', '0', 2, '', '2025-12-18 16:49:29', '', '2025-12-18 16:49:28', 'admin', '2025-12-18 22:02:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (33, NULL, 'yan17', 'yan17', '00', '', '', '0', '', '$2b$12$pgnqNqszYtbluAE4QBq3iuz9TWONrctog3Z54.2f.vun3mmcys5PK', '0', 2, '', NULL, '', '2025-12-18 21:52:28', 'admin', '2025-12-18 22:02:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (34, NULL, 'luping', 'luping', '00', '', '', '0', '', '$2b$12$gOIzkwAWgPzj/PvPYKuNne/J/z0Db25qMcDG.T8n30FY63YZk7YZu', '0', 2, '', '2025-12-18 21:57:42', '', '2025-12-18 21:57:41', 'admin', '2025-12-18 22:02:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (35, NULL, 'ahao', 'ahao', '00', '', '', '0', '', '$2b$12$OTcN42NSgcXpEneKCqU8f.KioZm4jIQ.yyPO.KtQnf1MOrCp.7WiO', '0', 2, '', '2025-12-18 22:08:04', '', '2025-12-18 22:05:45', 'admin', '2025-12-18 23:38:25', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (36, NULL, 'gqiao', 'gqiao', '00', '', '', '0', '', '$2b$12$pG2QijR8oFWm0ICVMJ3EXOKbdHeyLruuFI1gMC2I9rBi5o7AZOicu', '0', 2, '', '2025-12-18 22:09:12', '', '2025-12-18 22:09:10', 'admin', '2025-12-18 23:38:25', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (37, NULL, 'bli', 'bli', '00', '', '', '0', '', '$2b$12$3Vbkeuynq0qAhNcQ3I7wu.MFzeqj1UhcpZ3uq3mfzYpQ5w.5a47yC', '0', 0, '', '2025-12-18 22:25:26', '', '2025-12-18 22:25:18', '', '2025-12-18 22:25:18', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (38, NULL, 'vfang', 'vfang', '00', '', '', '0', '', '$2b$12$XdjL36qjabWSZ74R2GqLRe8C/BNooQSla0wBk.FHXLJKUrUM1L3ve', '0', 0, '', '2025-12-18 22:27:46', '', '2025-12-18 22:27:42', '', '2025-12-18 22:27:42', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (39, NULL, 'nawang', 'nawang', '00', '', '', '0', '', '$2b$12$xRwYQqcaggIOhBq67I01Z.62xQ53ky.Wag2DkisZ3tuI5NaANQJEO', '0', 0, '', NULL, '', '2025-12-18 23:02:10', '', '2025-12-18 23:02:10', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (40, NULL, 'oqin', 'oqin', '00', '', '', '0', '', '$2b$12$cejRKUVfck1BEsjMhoTV1.qzdkQxVhQkUtwk.efGXjw3d5lrzWJlq', '0', 0, '', NULL, '', '2025-12-18 23:38:19', '', '2025-12-18 23:38:19', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (41, NULL, 'yong03', 'yong03', '00', '', '', '0', '', '$2b$12$ji8RSpyuudoU33UbN.qSw.es0KLnsAhCJQaPeMsKUaWc4to5Jvhu2', '0', 2, '', NULL, '', '2025-12-18 23:39:09', 'admin', '2025-12-18 23:39:15', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (42, NULL, 'haoqiang', 'haoqiang', '00', '', '', '0', '', '$2b$12$oyV.gTlOLhA76U.FOkttW.5CrklJqN0XkadgYfsguH7Tuj6pH6qyC', '0', 2, '', NULL, '', '2025-12-18 23:40:26', 'admin', '2025-12-18 23:40:31', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (43, NULL, 'jing71', 'jing71', '00', '', '', '0', '', '$2b$12$4QSMUGpRcm5/.OSjpx4DMOQ5f9nJuXr0TiwcdpQC/6Si/z6mo1nPa', '0', 2, '', NULL, '', '2025-12-18 23:40:54', 'admin', '2025-12-18 23:40:59', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (44, NULL, 'jun76', 'jun76', '00', '', '', '0', '', '$2b$12$IGThkqM3DJL06f9LyODzbewI65CdRYXPBj3a/e6rl68vWaBZ87fue', '0', 0, '', NULL, '', '2025-12-19 09:12:45', '', '2025-12-19 09:12:45', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (45, NULL, 'cuixiuying', 'cuixiuying', '00', '', '', '0', '', '$2b$12$2vjdIevW69pYMwn8mewO2ud65smvlSe9tIJlg79a5bcneHH3CPNv2', '0', 0, '', NULL, '', '2025-12-19 09:13:06', '', '2025-12-19 09:13:06', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (46, NULL, 'cdong', 'cdong', '00', '', '', '0', '', '$2b$12$OBH9WTdzSqMYGGQe2qhRJuqDWxrCG6fzu8Bt.FhP8bb8WF.qAUQ/O', '0', 0, '', NULL, '', '2025-12-19 09:17:12', '', '2025-12-19 09:17:12', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (47, NULL, 'li69', 'li69', '00', '', '', '0', '', '$2b$12$fXkSbnBFisIeIh0.IMG53.vsvvtjJu2iEu8/1Iqr3LcpPYVLP3OrK', '0', 2, '', NULL, '', '2025-12-19 14:58:16', 'admin', '2025-12-19 14:58:20', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (48, NULL, 'sliao', 'sliao', '00', '', '', '0', '', '$2b$12$c8VNiHQIKxNX0Bwkk0Ws4eo5o8Z8enlnk779XCQUqQMQ4FYu8I8MS', '0', 0, '', NULL, '', '2025-12-22 11:52:55', '', '2025-12-22 11:52:55', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (49, NULL, 'rcheng', 'rcheng', '00', '', '', '0', '', '$2b$12$/cBtIHLe36umAGfzAhP9yeXFrgyoUuXJY3oFhmVw2FMYY5NS.SA4a', '0', 0, '', NULL, '', '2025-12-22 17:35:01', '', '2025-12-22 17:35:01', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (50, NULL, 'xiulantan', 'xiulantan', '00', '', '', '0', '', '$2b$12$OyMlgTP.yKYNjltnrS.bROhk9c5C0h1phlWIT8uE2zi4TA8M/Ausi', '0', 0, '', NULL, '', '2025-12-22 17:35:31', '', '2025-12-22 17:35:31', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (51, NULL, 'jingfu', 'jingfu', '00', '', '', '0', '', '$2b$12$kLBa7/uja1DneaJE7QYNLecZCtuXs/vMZHIwkNWeBYoFZKqCyeGQu', '0', 0, '', NULL, '', '2025-12-22 17:36:01', '', '2025-12-22 17:36:01', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (52, NULL, 'yshi', 'yshi', '00', '', '', '0', '', '$2b$12$cCnvFqdwZBBfb6aMgoNB4u/xbbPAw/CdWeBO1W8Tz.XEqBHK0areS', '0', 0, '', NULL, '', '2025-12-22 17:36:02', '', '2025-12-22 17:36:02', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (53, NULL, 'jing10', 'jing10', '00', '', '', '0', '', '$2b$12$cj.yhRgeFXESYnAFuLOkzeGaCl9MiGoRVj5htxkxE3hs1Gto6X4Iq', '0', 0, '', NULL, '', '2025-12-22 17:36:31', '', '2025-12-22 17:36:31', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (54, NULL, 'ztian', 'ztian', '00', '', '', '0', '', '$2b$12$MW7VuJ7OYfDpg/85OoA2buYhJx/mIBYM0NiuMGvE0uhTmpWExwMoq', '0', 0, '', NULL, '', '2025-12-22 17:38:31', '', '2025-12-22 17:38:31', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (55, NULL, 'huangming', 'huangming', '00', '', '', '0', '', '$2b$12$7oNkgyU6ejChxK3jq2jd9uc1SYpEkoigzSmMs14zvn.HH5CKnreee', '0', 0, '', NULL, '', '2025-12-22 17:39:31', '', '2025-12-22 17:39:31', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (56, NULL, 'gzhong', 'gzhong', '00', '', '', '0', '', '$2b$12$0NfxTd2GN0s1T2tkCXsMZ.jhyh.dZamk7ovfshE7rfdTPXrhdXDlK', '0', 0, '', NULL, '', '2025-12-22 17:39:32', '', '2025-12-22 17:39:32', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (57, NULL, 'oyang', 'oyang', '00', '', '', '0', '', '$2b$12$ROpMgyeoKAgqCucMdgvFuucWuI2wNCFW7olSHCk8j1pg0IhuuSNni', '0', 0, '', NULL, '', '2025-12-24 11:34:10', '', '2025-12-24 11:34:10', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (58, NULL, 'jiangjuan', 'jiangjuan', '00', '', '', '0', '', '$2b$12$w31oozZ62HVHuOtXdq2speC2iZtKYxzNQVFFtuSOXX/7qYXi82bEC', '0', 2, '', NULL, '', '2025-12-24 14:28:34', 'admin', '2025-12-24 14:28:36', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (59, NULL, 'taotan', 'taotan', '00', '', '', '0', '', '$2b$12$484PxevAYaGPa.6noj.5lemucoLiUPU/DmIY1xmi1fwQzigeh.d4e', '0', 2, '', NULL, '', '2025-12-24 14:29:48', 'admin', '2025-12-24 14:29:50', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (60, NULL, 'gangyuan', 'gangyuan', '00', '', '', '0', '', '$2b$12$mEm1RL53gvB/17.Xf/YxneObxD5FtuiLZYoA4kEHxuFU9W9cyOe0i', '0', 2, '', NULL, '', '2025-12-24 14:31:53', 'admin', '2025-12-24 14:31:55', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (61, NULL, 'lei58', 'lei58', '00', '', '', '0', '', '$2b$12$qHNtp3edG80igvqNMrOZiuYXwTHQexLnHah9ONEjFu0Vhfb.kB2UO', '0', 2, '', NULL, '', '2025-12-24 14:50:51', 'admin', '2025-12-24 14:50:53', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (62, NULL, 'jinglu', 'jinglu', '00', '', '', '0', '', '$2b$12$/1a.puJTsG0I94X4msPdrO2.X84HhJy64xEdTf.2NDrDQnWMIGOsK', '0', 2, '', NULL, '', '2025-12-24 14:52:10', 'admin', '2025-12-24 14:52:12', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (63, NULL, 'xcui', 'xcui', '00', '', '', '0', '', '$2b$12$FsHZN5te7ISItVeZfAT4Z.E78Dn.O15Kt3ZDbhsjguvCQQIRzz30G', '0', 0, '', NULL, '', '2025-12-24 15:00:09', '', '2025-12-24 15:00:09', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (64, NULL, 'ming58', 'ming58', '00', '', '', '0', '', '$2b$12$SCjSHgNrIqlVEZlGrXOGcekr0JBIZei0EFXGeH6BhFPEMCTGniLtC', '0', 2, '', NULL, '', '2025-12-24 15:05:45', 'admin', '2025-12-24 15:05:47', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (65, NULL, 'sfang', 'sfang', '00', '', '', '0', '', '$2b$12$1ISzKvubCq/ZVCAU4g1D0uVzTIjRHK1iCI3QnCTNzc20gOiy70.ba', '0', 0, '', '2025-12-24 15:06:29', '', '2025-12-24 15:06:01', '', '2025-12-24 15:06:01', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (66, NULL, 'xiulanhan', 'xiulanhan', '00', '', '', '0', '', '$2b$12$zsSnf5Eb7oldcqYjI5xCqu/49VHtcy5pFdOZTURkU7be6hDophqvW', '0', 2, '', '2025-12-24 15:06:34', '', '2025-12-24 15:06:34', 'admin', '2025-12-24 15:06:36', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (67, NULL, 'fma', 'fma', '00', '', '', '0', '', '$2b$12$m3q5NrqLa066mS.XpXOjJOpJZeP7UStBUt/31U0/X6QcA7PyJzDA2', '0', 0, '', NULL, '', '2025-12-24 15:19:31', '', '2025-12-24 15:19:31', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (68, NULL, 'zoulei', 'zoulei', '00', '', '', '0', '', '$2b$12$XJd7hU5A0dXTgLqm5kzrEeCcc5D.q3gUSVaTk05V0wJhTKFB2lFzW', '0', 2, '', '2025-12-24 15:20:38', '', '2025-12-24 15:20:37', 'admin', '2025-12-24 15:20:40', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (69, NULL, 'wei73', 'wei73', '00', '', '', '0', '', '$2b$12$MbONIwpWBD86WdlgirbKHOnkWG9O8YwANiJkXQCgBjArkyu5vWy46', '0', 2, '', '2025-12-24 15:24:42', '', '2025-12-24 15:24:18', 'admin', '2025-12-24 15:24:57', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (70, NULL, 'caimin', 'caimin', '00', '', '', '0', '', '$2b$12$l159JhJV19RJuYYXjhQMB.M.geHKaVb6CHkejmpqdg30cTT8sP98O', '0', 2, '', '2025-12-24 15:29:58', '', '2025-12-24 15:29:57', 'admin', '2025-12-24 15:29:59', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (71, NULL, 'xia55', 'xia55', '00', '', '', '0', '', '$2b$12$aJet5wAfdBchZyW.pjbqG.a0tb6fq1nQf3QXjhQpu8vtAk9GR48EC', '0', 2, '', '2025-12-24 15:30:06', '', '2025-12-24 15:30:05', 'admin', '2025-12-24 15:30:07', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (72, NULL, 'mye', 'mye', '00', '', '', '0', '', '$2b$12$M5XEAbUNDrtvGD1UgqOSM.Bb31.HSP.U/AMFSxrioJm746h9NSruO', '0', 2, '', '2025-12-24 15:31:07', '', '2025-12-24 15:31:06', 'admin', '2025-12-24 15:31:08', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (73, NULL, 'linchao', 'linchao', '00', '', '', '0', '', '$2b$12$xwXfFobah7SRE/4jSGhE3.APpQjLdHZWS9BV19BzT0wMuIB1pNJ5y', '0', 0, '', NULL, '', '2025-12-24 15:38:33', '', '2025-12-24 15:38:33', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (74, NULL, 'xiajuan', 'xiajuan', '00', '', '', '0', '', '$2b$12$9TySDu61tzXJjEuf5UduRuLzrF/vV1jqvmFAjjO/.IvQadGk/ZrZ6', '0', 2, '', '2025-12-24 15:43:36', '', '2025-12-24 15:43:33', 'admin', '2025-12-24 15:43:42', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (75, NULL, 'jfu', 'jfu', '00', '', '', '0', '', '$2b$12$JFs4gLlPrOTcz.GEerLeGer6qzeAuk8o.CNBmT7/HlfJmepnKlxvW', '0', 2, '', '2025-12-24 15:44:13', '', '2025-12-24 15:44:12', 'admin', '2025-12-24 15:44:14', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (76, NULL, 'yong70', 'yong70', '00', '', '', '0', '', '$2b$12$UI3sdbnHaJ2vgjScVZHHx.Z77LkfwWlysRW76uw1S6nvPpYCnMNl.', '0', 0, '', '2025-12-24 15:44:47', '', '2025-12-24 15:44:46', '', '2025-12-24 15:44:46', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (77, NULL, 'tianqiang', 'tianqiang', '00', '', '', '0', '', '$2b$12$NnXKe1qAYpo1GB9RB6EVfOxpQiVjSN/D2Q6uxkPrOrTGZ3.DYJImm', '0', 0, '', '2025-12-24 15:46:00', '', '2025-12-24 15:46:00', '', '2025-12-24 15:46:00', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (78, NULL, 'jianggang', 'jianggang', '00', '', '', '0', '', '$2b$12$YZ4Dzow7xzWYH.afZnkU5ugq7KzVl75A8/H4Zg5SmU6Dicnf/BvnS', '0', 0, '', '2025-12-24 15:49:12', '', '2025-12-24 15:49:11', '', '2025-12-24 15:49:11', NULL, NULL, 1);
INSERT INTO `sys_user` VALUES (79, NULL, 'chao20', 'chao20', '00', '', '', '0', '', '$2b$12$P8aJgWnTtPC3WcchScCLi.mMS79pyfKUUOO.21RT9H6UcSYig3fUq', '0', 0, '', '2025-12-24 16:06:03', '', '2025-12-24 16:06:02', '', '2025-12-24 16:06:02', NULL, NULL, 1);

-- ----------------------------
-- Table structure for sys_user_post
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_post`;
CREATE TABLE `sys_user_post`  (
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `post_id` bigint(20) NOT NULL COMMENT '岗位ID',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`user_id`, `post_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_post
-- ----------------------------
INSERT INTO `sys_user_post` VALUES (1, 1, '', '2025-08-22 15:28:53', '', '2025-08-22 15:28:53', NULL, NULL, 1, 0);
INSERT INTO `sys_user_post` VALUES (2, 2, '', '2025-07-30 06:15:43', '', '2025-07-30 06:15:43', NULL, NULL, NULL, 0);

-- ----------------------------
-- Table structure for sys_user_role
-- ----------------------------
DROP TABLE IF EXISTS `sys_user_role`;
CREATE TABLE `sys_user_role`  (
  `user_id` bigint(20) NOT NULL COMMENT '用户ID',
  `role_id` bigint(20) NOT NULL COMMENT '角色ID',
  `create_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '创建者',
  `create_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_by` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '更新者',
  `update_time` datetime NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `remark` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '备注',
  `description` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '描述',
  `sort_no` float NULL DEFAULT NULL COMMENT '排序值',
  `del_flag` int(11) NULL DEFAULT NULL COMMENT '删除标志 0正常 1删除 2代表删除',
  PRIMARY KEY (`user_id`, `role_id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user_role
-- ----------------------------
INSERT INTO `sys_user_role` VALUES (1, 1, '', '2025-08-22 15:28:53', '', '2025-08-22 15:28:53', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (2, 2, '', '2025-07-30 06:15:43', '', '2025-07-30 06:15:43', NULL, NULL, NULL, 0);
INSERT INTO `sys_user_role` VALUES (3, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO `sys_user_role` VALUES (10, 2, '', '2025-08-09 02:14:36', '', '2025-08-09 02:14:36', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (11, 2, '', '2025-08-10 10:48:39', '', '2025-08-10 10:48:39', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (57, 2, '', '2025-12-24 11:34:10', '', '2025-12-24 11:34:10', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (56, 2, '', '2025-12-22 17:39:32', '', '2025-12-22 17:39:32', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (55, 2, '', '2025-12-22 17:39:31', '', '2025-12-22 17:39:31', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (37, 2, '', '2025-12-18 22:25:18', '', '2025-12-18 22:25:18', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (38, 2, '', '2025-12-18 22:27:42', '', '2025-12-18 22:27:42', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (39, 2, '', '2025-12-18 23:02:10', '', '2025-12-18 23:02:10', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (40, 2, '', '2025-12-18 23:38:19', '', '2025-12-18 23:38:19', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (44, 2, '', '2025-12-19 09:12:45', '', '2025-12-19 09:12:45', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (45, 2, '', '2025-12-19 09:13:06', '', '2025-12-19 09:13:06', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (46, 2, '', '2025-12-19 09:17:12', '', '2025-12-19 09:17:12', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (48, 2, '', '2025-12-22 11:52:55', '', '2025-12-22 11:52:55', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (49, 2, '', '2025-12-22 17:35:01', '', '2025-12-22 17:35:01', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (50, 2, '', '2025-12-22 17:35:31', '', '2025-12-22 17:35:31', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (51, 2, '', '2025-12-22 17:36:01', '', '2025-12-22 17:36:01', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (52, 2, '', '2025-12-22 17:36:02', '', '2025-12-22 17:36:02', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (53, 2, '', '2025-12-22 17:36:31', '', '2025-12-22 17:36:31', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (54, 2, '', '2025-12-22 17:38:31', '', '2025-12-22 17:38:31', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (63, 2, '', '2025-12-24 15:00:09', '', '2025-12-24 15:00:09', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (65, 2, '', '2025-12-24 15:06:01', '', '2025-12-24 15:06:01', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (67, 2, '', '2025-12-24 15:19:31', '', '2025-12-24 15:19:31', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (73, 2, '', '2025-12-24 15:38:33', '', '2025-12-24 15:38:33', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (76, 2, '', '2025-12-24 15:44:46', '', '2025-12-24 15:44:46', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (77, 2, '', '2025-12-24 15:46:00', '', '2025-12-24 15:46:00', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (78, 2, '', '2025-12-24 15:49:11', '', '2025-12-24 15:49:11', NULL, NULL, 1, 0);
INSERT INTO `sys_user_role` VALUES (79, 2, '', '2025-12-24 16:06:02', '', '2025-12-24 16:06:02', NULL, NULL, 1, 0);

SET FOREIGN_KEY_CHECKS = 1;
