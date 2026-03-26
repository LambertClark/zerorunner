-- PC 素材绑定关系回填脚本
-- 用途：为已存在的 pc_case 记录，根据 step_data 中的图片字段补建 pc_picture_binding 记录
-- 执行前提：pc_picture_info 表已有对应 URL 记录
-- 使用方式：在 MySQL 中直接执行，或通过迁移框架执行

-- 1. 建表（若不存在）
CREATE TABLE IF NOT EXISTS `pc_picture_info` (
  `id`            BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name`          VARCHAR(255) NOT NULL                COMMENT '素材名称',
  `url`           TEXT         NOT NULL                COMMENT '素材URL',
  `tag_id`        BIGINT                               COMMENT '标签节点ID',
  `project_id`    INT                                  COMMENT '项目ID',
  `remarks`       VARCHAR(255)                         COMMENT '备注',
  `creation_date` DATETIME     DEFAULT NOW()           COMMENT '创建时间',
  `created_by`    BIGINT                               COMMENT '创建人ID',
  `updation_date` DATETIME     DEFAULT NOW()           COMMENT '更新时间',
  `updated_by`    BIGINT                               COMMENT '更新人ID',
  `enabled_flag`  TINYINT(1)   DEFAULT 1 NOT NULL      COMMENT '是否删除 0删除 1正常',
  `trace_id`      VARCHAR(255)                         COMMENT 'trace_id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC素材信息表';

CREATE TABLE IF NOT EXISTS `pc_picture_tag_tree` (
  `id`            BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name`          VARCHAR(255) NOT NULL                COMMENT '节点名称',
  `parent_id`     BIGINT       DEFAULT 0               COMMENT '父节点ID',
  `project_id`    INT                                  COMMENT '项目ID',
  `remarks`       VARCHAR(255)                         COMMENT '备注',
  `creation_date` DATETIME     DEFAULT NOW()           COMMENT '创建时间',
  `created_by`    BIGINT                               COMMENT '创建人ID',
  `updation_date` DATETIME     DEFAULT NOW()           COMMENT '更新时间',
  `updated_by`    BIGINT                               COMMENT '更新人ID',
  `enabled_flag`  TINYINT(1)   DEFAULT 1 NOT NULL      COMMENT '是否删除',
  `trace_id`      VARCHAR(255)                         COMMENT 'trace_id',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC素材标签树';

CREATE TABLE IF NOT EXISTS `pc_picture_binding` (
  `id`            BIGINT       NOT NULL AUTO_INCREMENT COMMENT '主键',
  `picture_id`    BIGINT       NOT NULL                COMMENT '素材ID',
  `table_type`    VARCHAR(32)  NOT NULL                COMMENT '绑定类型 case/tree',
  `table_id`      BIGINT       NOT NULL                COMMENT '绑定对象ID',
  `creation_date` DATETIME     DEFAULT NOW()           COMMENT '创建时间',
  `created_by`    BIGINT                               COMMENT '创建人ID',
  `updation_date` DATETIME     DEFAULT NOW()           COMMENT '更新时间',
  `updated_by`    BIGINT                               COMMENT '更新人ID',
  `enabled_flag`  TINYINT(1)   DEFAULT 1 NOT NULL      COMMENT '是否删除',
  `trace_id`      VARCHAR(255)                         COMMENT 'trace_id',
  PRIMARY KEY (`id`),
  INDEX `idx_picture_id` (`picture_id`),
  INDEX `idx_table` (`table_type`, `table_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC素材绑定关系表';

-- 2. 其余 PC 核心表 DDL
CREATE TABLE IF NOT EXISTS `pc_devices` (
  `id`             BIGINT       NOT NULL AUTO_INCREMENT,
  `name`           VARCHAR(255) NOT NULL               COMMENT '设备名称',
  `identity`       VARCHAR(255) NOT NULL UNIQUE         COMMENT '设备唯一标识',
  `ipv4_addresses` VARCHAR(1024)                       COMMENT 'IP列表逗号分隔',
  `port`           INT          DEFAULT 8088            COMMENT 'Agent端口',
  `remarks`        TEXT,
  `creation_date`  DATETIME     DEFAULT NOW(),
  `created_by`     BIGINT,
  `updation_date`  DATETIME     DEFAULT NOW(),
  `updated_by`     BIGINT,
  `enabled_flag`   TINYINT(1)   DEFAULT 1 NOT NULL,
  `trace_id`       VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC执行设备表';

CREATE TABLE IF NOT EXISTS `pc_case` (
  `id`                  BIGINT       NOT NULL AUTO_INCREMENT,
  `name`                VARCHAR(255) NOT NULL             COMMENT '用例名称',
  `project_id`          INT,
  `module_id`           INT,
  `pc_device_identity`  VARCHAR(255)                      COMMENT '绑定执行设备标识',
  `step_data`           JSON                              COMMENT '步骤树',
  `tags`                JSON,
  `remarks`             TEXT,
  `creation_date`       DATETIME     DEFAULT NOW(),
  `created_by`          BIGINT,
  `updation_date`       DATETIME     DEFAULT NOW(),
  `updated_by`          BIGINT,
  `enabled_flag`        TINYINT(1)   DEFAULT 1 NOT NULL,
  `trace_id`            VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC自动化用例表';

CREATE TABLE IF NOT EXISTS `pc_reports` (
  `id`              BIGINT       NOT NULL AUTO_INCREMENT,
  `report_name`     VARCHAR(255)                          COMMENT '报告名称',
  `case_id`         BIGINT,
  `case_name`       VARCHAR(255),
  `project_id`      INT,
  `status`          INT          DEFAULT 2                COMMENT '0失败 1成功 2执行中',
  `success`         TINYINT(1),
  `duration`        INT          DEFAULT 0                COMMENT '总耗时ms',
  `detail_table`    VARCHAR(64),
  `executor_id`     BIGINT,
  `device_identity` VARCHAR(255),
  `creation_date`   DATETIME     DEFAULT NOW(),
  `created_by`      BIGINT,
  `updation_date`   DATETIME     DEFAULT NOW(),
  `updated_by`      BIGINT,
  `enabled_flag`    TINYINT(1)   DEFAULT 1 NOT NULL,
  `trace_id`        VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC用例执行报告主表';

-- 分表 pc_report_detail_0 ~ pc_report_detail_9
-- 用循环语句替代（MySQL 存储过程方式，或手动执行10次）
-- 以下仅展示第 0 张，其余同理替换数字

CREATE TABLE IF NOT EXISTS `pc_report_detail_0` (
  `id`                BIGINT       NOT NULL AUTO_INCREMENT,
  `report_id`         BIGINT                              COMMENT '报告ID',
  `case_id`           BIGINT,
  `step_id`           BIGINT,
  `report_name`       VARCHAR(255),
  `operation_state`   VARCHAR(64),
  `operation_type`    VARCHAR(64),
  `expect_value`      TEXT,
  `actual_value`      TEXT,
  `state_image`       TEXT,
  `exception_message` TEXT,
  `error_type`        VARCHAR(128),
  `operation_context` TEXT,
  `success`           TINYINT(1),
  `original_image_path` TEXT,
  `duration`          INT          DEFAULT 0,
  `is_template`       TINYINT(1)   DEFAULT 0,
  `creation_date`     DATETIME     DEFAULT NOW(),
  `created_by`        BIGINT,
  `updation_date`     DATETIME     DEFAULT NOW(),
  `updated_by`        BIGINT,
  `enabled_flag`      TINYINT(1)   DEFAULT 1 NOT NULL,
  `trace_id`          VARCHAR(255),
  PRIMARY KEY (`id`),
  INDEX `idx_report_id` (`report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 重复上面建表语句，表名分别改为 pc_report_detail_1 ~ pc_report_detail_9

CREATE TABLE IF NOT EXISTS `pc_plan` (
  `id`                  BIGINT       NOT NULL AUTO_INCREMENT,
  `name`                VARCHAR(255) NOT NULL,
  `project_id`          INT,
  `case_ids`            JSON,
  `pc_device_identity`  VARCHAR(255),
  `remarks`             TEXT,
  `creation_date`       DATETIME     DEFAULT NOW(),
  `created_by`          BIGINT,
  `updation_date`       DATETIME     DEFAULT NOW(),
  `updated_by`          BIGINT,
  `enabled_flag`        TINYINT(1)   DEFAULT 1 NOT NULL,
  `trace_id`            VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC测试计划表';

CREATE TABLE IF NOT EXISTS `pc_plan_reports` (
  `id`             BIGINT       NOT NULL AUTO_INCREMENT,
  `report_name`    VARCHAR(255),
  `plan_id`        BIGINT,
  `plan_name`      VARCHAR(255),
  `project_id`     INT,
  `status`         INT          DEFAULT 2,
  `success`        TINYINT(1),
  `duration`       INT          DEFAULT 0,
  `total_count`    INT          DEFAULT 0,
  `success_count`  INT          DEFAULT 0,
  `fail_count`     INT          DEFAULT 0,
  `executor_id`    BIGINT,
  `device_identity` VARCHAR(255),
  `creation_date`  DATETIME     DEFAULT NOW(),
  `created_by`     BIGINT,
  `updation_date`  DATETIME     DEFAULT NOW(),
  `updated_by`     BIGINT,
  `enabled_flag`   TINYINT(1)   DEFAULT 1 NOT NULL,
  `trace_id`       VARCHAR(255),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC计划执行报告主表';

CREATE TABLE IF NOT EXISTS `pc_plan_report_detail` (
  `id`              BIGINT       NOT NULL AUTO_INCREMENT,
  `plan_report_id`  BIGINT                               COMMENT '计划报告ID',
  `case_id`         BIGINT,
  `case_name`       VARCHAR(255),
  `report_id`       BIGINT,
  `status`          INT          DEFAULT 2,
  `success`         TINYINT(1),
  `duration`        INT          DEFAULT 0,
  `creation_date`   DATETIME     DEFAULT NOW(),
  `created_by`      BIGINT,
  `updation_date`   DATETIME     DEFAULT NOW(),
  `updated_by`      BIGINT,
  `enabled_flag`    TINYINT(1)   DEFAULT 1 NOT NULL,
  `trace_id`        VARCHAR(255),
  PRIMARY KEY (`id`),
  INDEX `idx_plan_report_id` (`plan_report_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='PC计划报告子用例明细表';
