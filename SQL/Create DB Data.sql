

-- 步骤 1: 创建并使用数据库
-- --------------------------------------------------------------------
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'MarketDB')
BEGIN
    CREATE DATABASE MarketDB;
    PRINT '数据库 [MarketDB] 创建成功。';
END
GO

USE MarketDB;
GO

-- 步骤 2: 清理旧表 (按与创建相反的顺序，避免外键冲突)
-- --------------------------------------------------------------------
PRINT '>>> 步骤 2: 清理并重建表...';
IF OBJECT_ID('dbo.BillItems', 'U') IS NOT NULL DROP TABLE dbo.BillItems;
IF OBJECT_ID('dbo.Bills', 'U') IS NOT NULL DROP TABLE dbo.Bills;
IF OBJECT_ID('dbo.Products', 'U') IS NOT NULL DROP TABLE dbo.Products;
IF OBJECT_ID('dbo.Categories', 'U') IS NOT NULL DROP TABLE dbo.Categories;
IF OBJECT_ID('dbo.Guests', 'U') IS NOT NULL DROP TABLE dbo.Guests;
IF OBJECT_ID('dbo.Employees', 'U') IS NOT NULL DROP TABLE dbo.Employees;

CREATE TABLE Employees (
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY, 
    Name NVARCHAR(100) NOT NULL, 
    Gender NVARCHAR(4), 
    BirthDate DATE NOT NULL, 
    Position NVARCHAR(50) NOT NULL, 
    Phone NVARCHAR(20) UNIQUE,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(128) NOT NULL,
    role NVARCHAR(20) NOT NULL DEFAULT 'cashier'
);
CREATE TABLE Guests (
    GuestID INT IDENTITY(1,1) PRIMARY KEY, 
	Name NVARCHAR(100) NOT NULL, 
    MembershipID NVARCHAR(50), 
	Points INT DEFAULT 0
);
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    Name NVARCHAR(100) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL,
    Stock INT DEFAULT 0,
    Unit NVARCHAR(10),
    LastInDate DATETIME,
    Category NVARCHAR(50) NOT NULL  
);
CREATE TABLE Bills (
    BillID INT IDENTITY(1,1) PRIMARY KEY, 
	TotalAmount DECIMAL(10, 2) NOT NULL, 
	Status NVARCHAR(20) NOT NULL DEFAULT '未结账'
	CONSTRAINT CK_Bills_Status CHECK (Status IN ('已结账', '未结账')),
    BillDate DATETIME DEFAULT GETDATE(), 
	EmployeeID INT NOT NULL, 
	GuestID INT,
	PaymentMethod NVARCHAR(20) NOT NULL DEFAULT '现金'
	CONSTRAINT CK_Bills_PaymentMethod CHECK (PaymentMethod IN ('现金', '银行卡', '微信支付', '支付宝')),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID), 
	FOREIGN KEY (GuestID) REFERENCES Guests(GuestID)
);
CREATE TABLE BillItems (
    BillItemID INT IDENTITY(1,1) PRIMARY KEY, 
	BillID INT NOT NULL, 
	ProductID INT NOT NULL,
    Quantity INT NOT NULL, 
	Price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (BillID) REFERENCES Bills(BillID), 
	FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
PRINT '>>> 表结构已准备就绪。';
GO

-- 步骤 3: 插入丰富后的基础数据
-- --------------------------------------------------------------------
PRINT '>>> 步骤 3: 插入丰富后的基础数据...';

INSERT INTO Employees (Name, Gender, BirthDate, Position, Phone, username, password, role) VALUES
(N'张三', N'男', '1990-05-15', N'收银员', '13800138001', 'cashier1', 'cashier123', 'cashier'),      -- 【收银员】特有页面“收银台”“订单管理”
(N'李四', N'女', '1988-10-20', N'理货员', '13900139002', 'stocker1', 'stocker123', 'stocker'),        -- 【理货员】特有页面“商品管理”
(N'王芳', N'女', '1995-03-12', N'仓管员', '13700137003', 'warehouse1', 'warehouse123', 'warehouse'),  -- 【仓管员】特有页面“库存管理”
(N'刘军', N'男', '1985-07-05', N'管理员', '13600136004', 'admin1', 'admin123', 'admin'),              -- 【管理员】拥有全部页面
(N'张建军', N'男', '1980-01-01', N'管理员', '13900000001', 'admin2', 'admin123', 'admin'),             -- 管理员
(N'李海燕', N'女', '1982-02-02', N'管理员', '13900000002', 'admin3', 'admin123', 'admin');             -- 管理员

-- 插入顾客数据
INSERT INTO Guests (Name, MembershipID, Points) VALUES
(N'李华', 'V000001', 800),    -- ID=1
(N'张伟', 'V000002', 1200),   -- ID=2
(N'王丽', NULL, 300),        -- ID=3 (非会员)
(N'郑强', 'V000005', 2000),   -- ID=4
(N'孙颖', 'V000006', 750),    -- ID=5
(N'黄丽', NULL, 0);          -- ID=6 (非会员)

-- 插入商品数据
INSERT INTO Products (Name, Category, Price, Stock, Unit) VALUES
(N'苹果', N'水果', 6.50, 120, N'箱'),
(N'香蕉', N'水果', 3.99, 150, N'把'),
(N'牛奶', N'饮品', 4.50, 250, N'箱'),
(N'可乐', N'饮品', 3.00, 300, N'罐'),
(N'薯片', N'零食', 5.20, 220, N'袋'),
(N'面包', N'食品', 6.80, 80, N'袋'),
(N'鸡蛋', N'食品', 8.90, 180, N'盒'),
(N'洗发水', N'日用品', 29.90, 95, N'瓶'),
(N'香皂', N'日用品', 3.50, 160, N'块'),
(N'卫生纸', N'日用品', 15.80, 110, N'提'),
(N'牙膏', N'日用品', 12.80, 120, N'支'),
(N'牛肉', N'生鲜', 49.90, 75, N'公斤'),
(N'大米', N'粮食', 35.90, 60, N'袋'),
(N'面粉', N'粮食', 22.50, 40, N'袋');

PRINT '>>> 基础数据插入完毕。';
GO


-- 步骤 4: 创建订单场景 (使用新数据)
-- --------------------------------------------------------------------
PRINT '>>> 步骤 4: 创建订单场景...';

-- 场景 1: 顾客"李华"由员工"张三"处理的一笔小额订单
BEGIN TRANSACTION;
    DECLARE @GuestID_1 INT, @EmployeeID_1 INT, @Product_Apple INT, @Product_Milk INT, @BillID_1 INT;
    SELECT @GuestID_1 = GuestID FROM Guests WHERE Name = N'李华';
    SELECT @EmployeeID_1 = EmployeeID FROM Employees WHERE Name = N'张三';
    SELECT @Product_Apple = ProductID FROM Products WHERE Name = N'苹果';
    SELECT @Product_Milk = ProductID FROM Products WHERE Name = N'牛奶';

    INSERT INTO Bills (TotalAmount, Status, EmployeeID, GuestID) VALUES (28.50, N'已结账', @EmployeeID_1, @GuestID_1);
    SET @BillID_1 = SCOPE_IDENTITY();
    INSERT INTO BillItems(BillID, ProductID, Quantity, Price) VALUES
    (@BillID_1, @Product_Apple, 3, 6.50),
    (@BillID_1, @Product_Milk, 2, 4.50);
COMMIT TRANSACTION;
PRINT '>>> 订单 1 创建成功。';
GO

-- 场景 2: 新顾客"郑强"(VIP)由员工"王芳"处理的一笔大额订单, 购买了生鲜和日化用品
BEGIN TRANSACTION;
    DECLARE @GuestID_2 INT, @EmployeeID_2 INT, @Product_Beef INT, @Product_Shampoo INT, @BillID_2 INT;
    SELECT @GuestID_2 = GuestID FROM Guests WHERE Name = N'郑强';
    SELECT @EmployeeID_2 = EmployeeID FROM Employees WHERE Name = N'王芳';
    SELECT @Product_Beef = ProductID FROM Products WHERE Name = N'牛肉';
    SELECT @Product_Shampoo = ProductID FROM Products WHERE Name = N'洗发水';

    INSERT INTO Bills (TotalAmount, Status, EmployeeID, GuestID) VALUES (129.70, N'已结账', @EmployeeID_2, @GuestID_2);
    SET @BillID_2 = SCOPE_IDENTITY();
    INSERT INTO BillItems(BillID, ProductID, Quantity, Price) VALUES
    (@BillID_2, @Product_Beef, 2, 49.90),    -- 2公斤牛肉
    (@BillID_2, @Product_Shampoo, 1, 29.90); -- 1瓶洗发水
COMMIT TRANSACTION;
PRINT '>>> 订单 2 创建成功。';
GO

-- 场景 3: 新顾客"黄丽"(非会员)由员工"张三"处理的订单, 处于"未结账"状态
BEGIN TRANSACTION;
    DECLARE @GuestID_3 INT, @EmployeeID_3 INT, @Product_Coke INT, @Product_Bread INT, @BillID_3 INT;
    SELECT @GuestID_3 = GuestID FROM Guests WHERE Name = N'黄丽';
    SELECT @EmployeeID_3 = EmployeeID FROM Employees WHERE Name = N'张三';
    SELECT @Product_Coke = ProductID FROM Products WHERE Name = N'可乐';
    SELECT @Product_Bread = ProductID FROM Products WHERE Name = N'面包';

    INSERT INTO Bills (TotalAmount, Status, EmployeeID, GuestID) VALUES (15.80, N'未结账', @EmployeeID_3, @GuestID_3);
    SET @BillID_3 = SCOPE_IDENTITY();
    INSERT INTO BillItems(BillID, ProductID, Quantity, Price) VALUES
    (@BillID_3, @Product_Coke, 3, 3.00),     -- 3罐可乐
    (@BillID_3, @Product_Bread, 1, 6.80);    -- 1袋面包
COMMIT TRANSACTION;
PRINT '>>> 订单 3 创建成功。';
GO


-- 步骤 5: 验证所有数据
-- --------------------------------------------------------------------
PRINT '>>> 步骤 5: 验证所有数据插入结果...';
SELECT '员工表' as 表名, * FROM Employees;
SELECT '顾客表' as 表名, * FROM Guests;
SELECT '商品表' as 表名, * FROM Products;
SELECT '账单主表' as 表名, * FROM Bills;
SELECT '账单明细表' as 表名, * FROM BillItems;
GO

PRINT '>>> 所有数据已按正确顺序丰富并插入完毕！';
GO