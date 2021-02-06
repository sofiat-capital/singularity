
use sofiat;

CREATE VIEW vOrderQueue (idorderqeue, ticker, side, timeCreated, price)
AS
SELECT 
	orderQueue.idorderqueue,
    product.ticker,
    orderQueue.side,
    orderQueue.timeCreated,
    orderQueue.price
FROM orderQueue, product
ORDER BY timeCreated DESC;