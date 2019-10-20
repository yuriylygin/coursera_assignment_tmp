use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select name from store where is_automated = 1;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct store_id from sale;


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select distinct store.store_id from store
    left join sale on store.store_id = sale.store_id
    where sale.store_id is null;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.select ...
select product.name, avg(sale.total/sale.quantity) from sale
    join product using(product_id)
    group by sale.product_id;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select product.name from sale
    join product using(product_id) 
    group by product_id
    order by count(distinct sale.store_id) limit 1;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select store.name from sale 
    natural join store 
    group by sale.store_id
    order by count(distinct sale.product_id) limit 1;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
select * from sale order by total desc limit 1;

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select date from sale order by total desc, date limit 1;
