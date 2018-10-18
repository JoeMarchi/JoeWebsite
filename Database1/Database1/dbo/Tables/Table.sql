CREATE TABLE [dbo].[Table] (
    [Id]           INT            NOT NULL,
    [Subject]      NVARCHAR (50)  NOT NULL,
    [Content]      NVARCHAR (MAX) NOT NULL,
    [PostDateTime] DATETIME       NOT NULL,
    PRIMARY KEY CLUSTERED ([Id] ASC)
);



