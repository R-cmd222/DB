

-- ���� 1: ������ʹ�����ݿ�
-- --------------------------------------------------------------------
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'MarketDB')
BEGIN
    CREATE DATABASE MarketDB;
    PRINT '���ݿ� [MarketDB] �����ɹ���';
END
GO

USE MarketDB;
GO

-- ���� 2: ����ɱ� (���봴���෴��˳�򣬱��������ͻ)
-- --------------------------------------------------------------------
PRINT '>>> ���� 2: �����ؽ���...';
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
	Status NVARCHAR(20) NOT NULL DEFAULT 'δ����'
	CONSTRAINT CK_Bills_Status CHECK (Status IN ('�ѽ���', 'δ����')),
    BillDate DATETIME DEFAULT GETDATE(), 
	EmployeeID INT NOT NULL, 
	GuestID INT,
	PaymentMethod NVARCHAR(20) NOT NULL DEFAULT '�ֽ�'
	CONSTRAINT CK_Bills_PaymentMethod CHECK (PaymentMethod IN ('�ֽ�', '���п�', '΢��֧��', '֧����')),
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
PRINT '>>> ��ṹ��׼��������';
GO

-- ���� 3: ����ḻ��Ļ�������
-- --------------------------------------------------------------------
PRINT '>>> ���� 3: ����ḻ��Ļ�������...';

INSERT INTO Employees (Name, Gender, BirthDate, Position, Phone, username, password, role) VALUES
(N'����', N'��', '1990-05-15', N'����Ա', '13800138001', 'cashier1', 'cashier123', 'cashier'),      -- ������Ա������ҳ�桰����̨������������
(N'����', N'Ů', '1988-10-20', N'���Ա', '13900139002', 'stocker1', 'stocker123', 'stocker'),        -- �����Ա������ҳ�桰��Ʒ����
(N'����', N'Ů', '1995-03-12', N'�ֹ�Ա', '13700137003', 'warehouse1', 'warehouse123', 'warehouse'),  -- ���ֹ�Ա������ҳ�桰������
(N'����', N'��', '1985-07-05', N'����Ա', '13600136004', 'admin1', 'admin123', 'admin'),              -- ������Ա��ӵ��ȫ��ҳ��
(N'�Ž���', N'��', '1980-01-01', N'����Ա', '13900000001', 'admin2', 'admin123', 'admin'),             -- ����Ա
(N'���', N'Ů', '1982-02-02', N'����Ա', '13900000002', 'admin3', 'admin123', 'admin');             -- ����Ա

-- ����˿�����
INSERT INTO Guests (Name, MembershipID, Points) VALUES
(N'�', 'V000001', 800),    -- ID=1
(N'��ΰ', 'V000002', 1200),   -- ID=2
(N'����', NULL, 300),        -- ID=3 (�ǻ�Ա)
(N'֣ǿ', 'V000005', 2000),   -- ID=4
(N'��ӱ', 'V000006', 750),    -- ID=5
(N'����', NULL, 0);          -- ID=6 (�ǻ�Ա)

-- ������Ʒ����
INSERT INTO Products (Name, Category, Price, Stock, Unit) VALUES
(N'ƻ��', N'ˮ��', 6.50, 120, N'��'),
(N'�㽶', N'ˮ��', 3.99, 150, N'��'),
(N'ţ��', N'��Ʒ', 4.50, 250, N'��'),
(N'����', N'��Ʒ', 3.00, 300, N'��'),
(N'��Ƭ', N'��ʳ', 5.20, 220, N'��'),
(N'���', N'ʳƷ', 6.80, 80, N'��'),
(N'����', N'ʳƷ', 8.90, 180, N'��'),
(N'ϴ��ˮ', N'����Ʒ', 29.90, 95, N'ƿ'),
(N'����', N'����Ʒ', 3.50, 160, N'��'),
(N'����ֽ', N'����Ʒ', 15.80, 110, N'��'),
(N'����', N'����Ʒ', 12.80, 120, N'֧'),
(N'ţ��', N'����', 49.90, 75, N'����'),
(N'����', N'��ʳ', 35.90, 60, N'��'),
(N'���', N'��ʳ', 22.50, 40, N'��');

PRINT '>>> �������ݲ�����ϡ�';
GO


-- ���� 4: ������������ (ʹ��������)
-- --------------------------------------------------------------------
PRINT '>>> ���� 4: ������������...';

-- ���� 1: �˿�"�"��Ա��"����"�����һ��С���
BEGIN TRANSACTION;
    DECLARE @GuestID_1 INT, @EmployeeID_1 INT, @Product_Apple INT, @Product_Milk INT, @BillID_1 INT;
    SELECT @GuestID_1 = GuestID FROM Guests WHERE Name = N'�';
    SELECT @EmployeeID_1 = EmployeeID FROM Employees WHERE Name = N'����';
    SELECT @Product_Apple = ProductID FROM Products WHERE Name = N'ƻ��';
    SELECT @Product_Milk = ProductID FROM Products WHERE Name = N'ţ��';

    INSERT INTO Bills (TotalAmount, Status, EmployeeID, GuestID) VALUES (28.50, N'�ѽ���', @EmployeeID_1, @GuestID_1);
    SET @BillID_1 = SCOPE_IDENTITY();
    INSERT INTO BillItems(BillID, ProductID, Quantity, Price) VALUES
    (@BillID_1, @Product_Apple, 3, 6.50),
    (@BillID_1, @Product_Milk, 2, 4.50);
COMMIT TRANSACTION;
PRINT '>>> ���� 1 �����ɹ���';
GO

-- ���� 2: �¹˿�"֣ǿ"(VIP)��Ա��"����"�����һ�ʴ���, ���������ʺ��ջ���Ʒ
BEGIN TRANSACTION;
    DECLARE @GuestID_2 INT, @EmployeeID_2 INT, @Product_Beef INT, @Product_Shampoo INT, @BillID_2 INT;
    SELECT @GuestID_2 = GuestID FROM Guests WHERE Name = N'֣ǿ';
    SELECT @EmployeeID_2 = EmployeeID FROM Employees WHERE Name = N'����';
    SELECT @Product_Beef = ProductID FROM Products WHERE Name = N'ţ��';
    SELECT @Product_Shampoo = ProductID FROM Products WHERE Name = N'ϴ��ˮ';

    INSERT INTO Bills (TotalAmount, Status, EmployeeID, GuestID) VALUES (129.70, N'�ѽ���', @EmployeeID_2, @GuestID_2);
    SET @BillID_2 = SCOPE_IDENTITY();
    INSERT INTO BillItems(BillID, ProductID, Quantity, Price) VALUES
    (@BillID_2, @Product_Beef, 2, 49.90),    -- 2����ţ��
    (@BillID_2, @Product_Shampoo, 1, 29.90); -- 1ƿϴ��ˮ
COMMIT TRANSACTION;
PRINT '>>> ���� 2 �����ɹ���';
GO

-- ���� 3: �¹˿�"����"(�ǻ�Ա)��Ա��"����"����Ķ���, ����"δ����"״̬
BEGIN TRANSACTION;
    DECLARE @GuestID_3 INT, @EmployeeID_3 INT, @Product_Coke INT, @Product_Bread INT, @BillID_3 INT;
    SELECT @GuestID_3 = GuestID FROM Guests WHERE Name = N'����';
    SELECT @EmployeeID_3 = EmployeeID FROM Employees WHERE Name = N'����';
    SELECT @Product_Coke = ProductID FROM Products WHERE Name = N'����';
    SELECT @Product_Bread = ProductID FROM Products WHERE Name = N'���';

    INSERT INTO Bills (TotalAmount, Status, EmployeeID, GuestID) VALUES (15.80, N'δ����', @EmployeeID_3, @GuestID_3);
    SET @BillID_3 = SCOPE_IDENTITY();
    INSERT INTO BillItems(BillID, ProductID, Quantity, Price) VALUES
    (@BillID_3, @Product_Coke, 3, 3.00),     -- 3�޿���
    (@BillID_3, @Product_Bread, 1, 6.80);    -- 1�����
COMMIT TRANSACTION;
PRINT '>>> ���� 3 �����ɹ���';
GO


-- ���� 5: ��֤��������
-- --------------------------------------------------------------------
PRINT '>>> ���� 5: ��֤�������ݲ�����...';
SELECT 'Ա����' as ����, * FROM Employees;
SELECT '�˿ͱ�' as ����, * FROM Guests;
SELECT '��Ʒ��' as ����, * FROM Products;
SELECT '�˵�����' as ����, * FROM Bills;
SELECT '�˵���ϸ��' as ����, * FROM BillItems;
GO

PRINT '>>> ���������Ѱ���ȷ˳��ḻ��������ϣ�';
GO