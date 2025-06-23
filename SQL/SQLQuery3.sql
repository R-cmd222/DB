

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
    EmployeeID INT IDENTITY(1,1) PRIMARY KEY, Name NVARCHAR(100) NOT NULL, Gender NVARCHAR(4), 
    BirthDate DATE NOT NULL, Position NVARCHAR(50) NOT NULL, Phone NVARCHAR(20) UNIQUE
);
CREATE TABLE Guests (
    GuestID INT IDENTITY(1,1) PRIMARY KEY, Name NVARCHAR(100) NOT NULL, 
    MembershipID NVARCHAR(50), Points INT DEFAULT 0
);
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY, Name NVARCHAR(100) NOT NULL UNIQUE
);
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY, Name NVARCHAR(100) NOT NULL, Price DECIMAL(10, 2) NOT NULL,
    Stock INT DEFAULT 0, Unit NVARCHAR(10), LastInDate DATETIME,
    CategoryID INT NOT NULL, FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);
CREATE TABLE Bills (
    BillID INT IDENTITY(1,1) PRIMARY KEY, TotalAmount DECIMAL(10, 2) NOT NULL, Status NVARCHAR(20),
    BillDate DATETIME DEFAULT GETDATE(), EmployeeID INT NOT NULL, GuestID INT,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID), FOREIGN KEY (GuestID) REFERENCES Guests(GuestID)
);
CREATE TABLE BillItems (
    BillItemID INT IDENTITY(1,1) PRIMARY KEY, BillID INT NOT NULL, ProductID INT NOT NULL,
    Quantity INT NOT NULL, Price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (BillID) REFERENCES Bills(BillID), FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
PRINT '>>> ��ṹ��׼��������';
GO

-- ���� 3: ����ḻ��Ļ�������
-- --------------------------------------------------------------------
PRINT '>>> ���� 3: ����ḻ��Ļ�������...';

-- ����Ա���͹���Ա����
INSERT INTO Employees (Name, Gender, BirthDate, Position, Phone) VALUES
(N'����', N'��', '1990-05-15', N'��������', '13800138001'), -- ID=1
(N'����', N'Ů', '1988-10-20', N'���Ա', '13900139002'), -- ID=2
(N'����', N'Ů', '1995-03-12', N'����Ա', '13700137003'), -- ID=3
(N'����', N'��', '1985-07-05', N'�ֹ�Ա', '13600136004'), -- ID=4
(N'�Ž���', N'��', '1980-01-01', N'����Ա', '13900000001'), -- ID=5
(N'���', N'Ů', '1982-02-02', N'����Ա', '13900000002'); -- ID=6

-- ����˿�����
INSERT INTO Guests (Name, MembershipID, Points) VALUES
(N'�', 'V000001', 800),    -- ID=1
(N'��ΰ', 'V000002', 1200),   -- ID=2
(N'����', NULL, 300),        -- ID=3 (�ǻ�Ա)
(N'֣ǿ', 'V000005', 2000),   -- ID=4
(N'��ӱ', 'V000006', 750),    -- ID=5
(N'����', NULL, 0);          -- ID=6 (�ǻ�Ա)

-- ������Ʒ��������
INSERT INTO Categories (Name) VALUES 
(N'ˮ��'), (N'��Ʒ'), (N'��ʳ'), (N'ʳƷ'), (N'�ջ�'), (N'����'), (N'��ʳ');

-- ������Ʒ����
INSERT INTO Products (Name, CategoryID, Price, Stock, Unit) VALUES
(N'ƻ��', 1, 6.50, 120, N'��'),     -- CategoryID=1
(N'�㽶', 1, 3.99, 150, N'��'),     -- CategoryID=1
(N'ţ��', 2, 4.50, 250, N'��'),     -- CategoryID=2
(N'����', 2, 3.00, 300, N'��'),     -- CategoryID=2
(N'��Ƭ', 3, 5.20, 220, N'��'),     -- CategoryID=3
(N'���', 4, 6.80, 80, N'��'),      -- CategoryID=4
(N'����', 4, 8.90, 180, N'��'),      -- CategoryID=4
(N'ϴ��ˮ', 5, 29.90, 95, N'ƿ'),    -- CategoryID=5
(N'����', 5, 3.50, 160, N'��'),     -- CategoryID=5
(N'����ֽ', 5, 15.80, 110, N'��'),    -- CategoryID=5
(N'����', 5, 12.80, 120, N'֧'),    -- CategoryID=5
(N'ţ��', 6, 49.90, 75, N'����'),   -- CategoryID=6
(N'����', 7, 35.90, 60, N'��'),     -- CategoryID=7
(N'���', 7, 22.50, 40, N'��');     -- CategoryID=7

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
SELECT '��Ʒ�����' as ����, * FROM Categories;
SELECT '��Ʒ��' as ����, * FROM Products;
SELECT '�˵�����' as ����, * FROM Bills;
SELECT '�˵���ϸ��' as ����, * FROM BillItems;
GO

PRINT '>>> ���������Ѱ���ȷ˳��ḻ��������ϣ�';
GO