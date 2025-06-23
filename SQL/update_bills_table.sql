-- 添加 PaymentMethod 列到 Bills 表
ALTER TABLE Bills
ADD PaymentMethod NVARCHAR(20) NOT NULL DEFAULT '现金';

-- 更新现有记录的支付方式
UPDATE Bills
SET PaymentMethod = '现金'
WHERE PaymentMethod IS NULL; 