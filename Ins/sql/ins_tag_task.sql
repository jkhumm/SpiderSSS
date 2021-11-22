/*
 Navicat Premium Data Transfer

 Source Server         : 148-master
 Source Server Type    : MySQL
 Source Server Version : 50735
 Source Host           : 192.168.1.148:3307
 Source Schema         : python-collect

 Target Server Type    : MySQL
 Target Server Version : 50735
 File Encoding         : 65001

 Date: 12/11/2021 10:22:25
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ins_tag_task
-- ----------------------------
DROP TABLE IF EXISTS `ins_tag_task`;
CREATE TABLE `ins_tag_task`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '业务id',
  `ins_tag_link` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ins帖子链接',
  `ins_account` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '明星ins账号',
  `is_crawled` tinyint(1) NOT NULL DEFAULT 0 COMMENT '0没爬取  1已爬取',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `tag_unique_index`(`ins_tag_link`, `ins_account`) USING BTREE COMMENT '明星帖子唯一索引'
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
