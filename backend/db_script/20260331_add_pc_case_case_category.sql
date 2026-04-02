-- 为 pc_case 表添加 case_category 字段（用例分类）
-- 兼容已有数据库的增量升级，可安全重复执行

-- 1. 若 case_category 列不存在则添加
SET @col_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME   = 'pc_case'
      AND COLUMN_NAME  = 'case_category'
);

SET @sql_add_col = IF(
    @col_exists = 0,
    'ALTER TABLE `pc_case` ADD COLUMN `case_category` VARCHAR(32) NULL COMMENT \'用例分类\' AFTER `module_id`',
    'SELECT 1'
);
PREPARE stmt FROM @sql_add_col;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- 2. 回填历史数据（置为默认分类 release）
UPDATE `pc_case`
SET `case_category` = 'release'
WHERE `case_category` IS NULL
   OR `case_category` = '';

-- 3. 收紧约束：NOT NULL + DEFAULT 'release'
ALTER TABLE `pc_case`
    MODIFY COLUMN `case_category` VARCHAR(32) NOT NULL DEFAULT 'release' COMMENT '用例分类';

-- 4. 若索引不存在则添加
SET @idx_exists = (
    SELECT COUNT(*)
    FROM information_schema.STATISTICS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME   = 'pc_case'
      AND INDEX_NAME   = 'idx_pc_case_case_category'
);

SET @sql_add_idx = IF(
    @idx_exists = 0,
    'ALTER TABLE `pc_case` ADD INDEX `idx_pc_case_case_category` (`case_category`)',
    'SELECT 1'
);
PREPARE stmt FROM @sql_add_idx;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;
