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

 Date: 22/11/2021 11:09:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ins_account_enums
-- ----------------------------
DROP TABLE IF EXISTS `ins_account_enums`;
CREATE TABLE `ins_account_enums`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '业务id',
  `ins_account` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '明星ins账号',
  `account_type` int(1) NOT NULL COMMENT '1穿搭 2品牌 3科技感 4自然 5宠物 6手工艺 7摄影 8其它',
  `ins_tag_count` int(11) NULL DEFAULT NULL COMMENT 'ins帖子数',
  `followers_count` int(11) NULL DEFAULT NULL COMMENT '粉丝数',
  `follow_count` int(11) NULL DEFAULT NULL COMMENT '关注数',
  `full_name` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '全民',
  `ins_id` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'ins上用户id',
  `create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT 'x修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 108 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '账号枚举表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ins_tag_info
-- ----------------------------
DROP TABLE IF EXISTS `ins_tag_info`;
CREATE TABLE `ins_tag_info`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '业务id',
  `ins_tag_link` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ins帖子链接',
  `ins_account` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '明星ins账号',
  `media_type` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '1单张图片 2多张图片 3视频',
  `likes_count` int(11) NULL DEFAULT 0 COMMENT '点赞数',
  `comments_count` int(11) NULL DEFAULT NULL COMMENT '评论数',
  `publish_time` datetime NULL DEFAULT NULL COMMENT '发布时间',
  `author_speak` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '作者发表的说说',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NULL DEFAULT NULL COMMENT '修改时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27449 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = 'ins上帖子的信息' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ins_tag_info_photo
-- ----------------------------
DROP TABLE IF EXISTS `ins_tag_info_photo`;
CREATE TABLE `ins_tag_info_photo`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '业务id',
  `ins_tag_link` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ins帖子链接',
  `photo_index` int(11) NOT NULL COMMENT '图片的位置index',
  `photo_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '图片/视频地址',
  `photo_height` int(11) NOT NULL COMMENT '图片高度',
  `photo_width` int(11) NULL DEFAULT NULL COMMENT '图片宽度',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ins_tag_link_index`(`ins_tag_link`) USING BTREE COMMENT 'ins链接地址普通索引'
) ENGINE = InnoDB AUTO_INCREMENT = 51322 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ins_tag_info_video
-- ----------------------------
DROP TABLE IF EXISTS `ins_tag_info_video`;
CREATE TABLE `ins_tag_info_video`  (
  `id` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '业务id',
  `ins_tag_link` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT 'ins帖子链接',
  `thumbnail_url` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '视频缩略图地址',
  `photo_height` int(11) NOT NULL COMMENT '图片高度',
  `photo_width` int(11) NOT NULL COMMENT '图片宽度',
  `video_url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '视频地址',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4931 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;