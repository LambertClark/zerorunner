-- pc_picture_info 绑定结构回填脚本
-- 用途：补齐 table_type / table_id 字段，并将历史 tree 素材回填到新绑定结构
SET NAMES utf8mb4;

-- 1. 检查并补齐 table_type 字段
SET @col_type_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME   = 'pc_picture_info'
      AND COLUMN_NAME  = 'table_type'
);

SET @sql1 = IF(
    @col_type_exists = 0,
    'ALTER TABLE pc_picture_info ADD COLUMN table_type VARCHAR(16) NULL COMMENT \'绑定类型：tree/case\'',
    'SELECT 1'
);
PREPARE stmt1 FROM @sql1;
EXECUTE stmt1;
DEALLOCATE PREPARE stmt1;

-- 2. 检查并补齐 table_id 字段
SET @col_id_exists = (
    SELECT COUNT(*)
    FROM information_schema.COLUMNS
    WHERE TABLE_SCHEMA = DATABASE()
      AND TABLE_NAME   = 'pc_picture_info'
      AND COLUMN_NAME  = 'table_id'
);

SET @sql2 = IF(
    @col_id_exists = 0,
    'ALTER TABLE pc_picture_info ADD COLUMN table_id BIGINT NULL COMMENT \'绑定对象id\'',
    'SELECT 1'
);
PREPARE stmt2 FROM @sql2;
EXECUTE stmt2;
DEALLOCATE PREPARE stmt2;

-- 3. 回填历史 tree 素材：table_type = 'tree', table_id = tree_id
UPDATE pc_picture_info
SET table_type = 'tree',
    table_id   = tree_id
WHERE enabled_flag = 1
  AND tree_id IS NOT NULL
  AND (
      table_type IS NULL
      OR (table_type = 'tree' AND table_id IS NULL)
  );

-- 4. 校验回填结果
SELECT COUNT(*) AS tree_binding_count
FROM pc_picture_info
WHERE enabled_flag = 1
  AND table_type   = 'tree'
  AND table_id     IS NOT NULL;
