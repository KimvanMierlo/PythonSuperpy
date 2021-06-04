This application can be used to keep track of your inventory. You can manage your profits and stock. The application can help you sell the first to expire products you have in stock. You can see wat you spent on the inventory and what you have earned with selling the products in your inventory. You can search profits of a specific date, or period.

There are five actions in the program: 
* buy
* sell
* inventory
* profit
* today. 
  
All actions have mandatory arguments and optional argument.

Note: Everytime you use an argument --date, --maxdate, --mindate you have to use the following format: yyyy-mm-dd or now (current date or date set by today function). 


# Buy

When you want to buy, the following arguments are mandatory: 
* --name, this is the name of the product
* --price, the purchase price of the product
* --expires, this is the date the product expires

Optional is 
* --amount, when you don't use the argument there is a default setting of 1.
  
### example
> buy --name chips --price 0.80  --expires 2023-11-23 --amount 500 


# inventory 

When you want to see your inventory, you can use the following optional arguments:
* --name, this is the name of the product
* --id, this is an unique number of a product in your inventory
* --date, this date refers to the date you bought the product for your inventory
* --mindate & maxdate, refers to a period you bought a product for your inventory


When you do not use these optional arguments the action inventory will show the whole inventory that you have in store.


### examples
Complete inventory:
>inventory

```
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|   id | name   |   amount |   price | date_expired   | date_bought   |   sold |   available | expired   |
+======+========+==========+=========+================+===============+========+=============+===========+
|    1 | cola   |       10 |    1.5  | 2023-12-25     | 2021-06-03    |     10 |           0 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    2 | cola   |        5 |    1.7  | 2023-11-23     | 2021-05-24    |      4 |           1 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    3 | chips  |        5 |    1.2  | 2023-11-23     | 2021-06-03    |      1 |           4 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    4 | chips  |      500 |    0.8  | 2023-11-23     | 2021-06-04    |      0 |         500 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    5 | cola   |      250 |    1    | 2023-11-23     | 2021-06-04    |      0 |         250 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    6 | beer   |      250 |    1.15 | 2023-11-23     | 2021-06-04    |      0 |         250 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    7 | beer   |      100 |    5    | 2022-06-30     | 2021-06-04    |      0 |         100 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    8 | wine   |      120 |    6.5  | 2024-01-31     | 2021-06-04    |      0 |         120 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    9 | nutes  |      150 |    1.95 | 2022-01-31     | 2021-06-04    |      0 |         150 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
```

Inventory of a specific product by name:
> inventory --name beer

```
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|   id | name   |   amount |   price | date_expired   | date_bought   |   sold |   available | expired   |
+======+========+==========+=========+================+===============+========+=============+===========+
|    6 | beer   |      250 |    1.15 | 2023-11-23     | 2021-06-04    |      0 |         250 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    7 | beer   |      100 |    5    | 2022-06-30     | 2021-06-04    |      0 |         100 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
```

Inventory bought on specific date
> inventory --date now
```
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    5 | cola   |      250 |    1    | 2023-11-23     | 2021-06-04    |      0 |         250 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    6 | beer   |      250 |    1.15 | 2023-11-23     | 2021-06-04    |      5 |         245 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    7 | beer   |      100 |    5    | 2022-06-30     | 2021-06-04    |      0 |         100 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    8 | wine   |      120 |    6.5  | 2024-01-31     | 2021-06-04    |      3 |         117 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    9 | nutes  |      150 |    1.95 | 2022-01-31     | 2021-06-04    |      0 |         150 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
``` 


When you search on a product name or id number that is not in inventory you will get no feedback.

# sell
Now that you have an inventory, you can sell your products. When you want to buy, the following arguments are mandatory: 
* --name, this is the name of the product you are selling
* --price, the selling price of the product


Optional is 
* --amount, when you don't use the argument there is a default setting of 1. 
* --id of the product you want to sell (only neccesairy if multiple items with the same name are available)
   
### Example:
> sell --name wine --price 8.99 --amount 3
For sell:
```
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|   id | name   |   amount |   price | date_expired   | date_bought   |   sold |   available | expired   |
+======+========+==========+=========+================+===============+========+=============+===========+
|    8 | wine   |      120 |     6.5 | 2024-01-31     | 2021-06-04    |      0 |         120 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
```
after sell:
> inventory --name wine
```
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|   id | name   |   amount |   price | date_expired   | date_bought   |   sold |   available | expired   |
+======+========+==========+=========+================+===============+========+=============+===========+
|    8 | wine   |      120 |     6.5 | 2024-01-31     | 2021-06-04    |      3 |         117 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
```

When a product is more than 1 time in your inventory list you must set the --id. When you did not set the --id, you will get the following notice:
> sell --name beer --price 3.99 --amount 5 

```
Multiple products found... Please specify the id:
+------+--------+----------+---------+----------------+---------------+--------+-------------+
|   id | name   |   amount |   price | date_expired   | date_bought   |   sold |   available |
+======+========+==========+=========+================+===============+========+=============+
|    6 | beer   |      250 |    1.15 | 2023-11-23     | 2021-06-04    |      0 |         250 |
+------+--------+----------+---------+----------------+---------------+--------+-------------+
|    7 | beer   |      100 |    5    | 2022-06-30     | 2021-06-04    |      0 |         100 |
+------+--------+----------+---------+----------------+---------------+--------+-------------+
```
You have to specify on id as follows:
> sell --name beer --price 3.99 --amount 5 --id 6

If you look in the inventory of the product, you can see that the beer with id number 6 has sold 5.
```
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|   id | name   |   amount |   price | date_expired   | date_bought   |   sold |   available | expired   |
+======+========+==========+=========+================+===============+========+=============+===========+
|    6 | beer   |      250 |    1.15 | 2023-11-23     | 2021-06-04    |      5 |         245 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
|    7 | beer   |      100 |    5    | 2022-06-30     | 2021-06-04    |      0 |         100 | False     |
+------+--------+----------+---------+----------------+---------------+--------+-------------+-----------+
```

When there is no more availble product, the following will be shown:
```
Product not available...
````

When a product is expired, the following wil be shown:
```
Product not available...
```

# Profit

When you want to see your profit, you can use the following optional arguments:
* --date, this is the exact date you want to use for reporting. When you type now it marks the current date (yyyy-mm-dd or now)
* --mindate & maxdate, you can use to mark a period (yyyy-mm-dd)
When you do not use these optional arguments the action profit will show the profit of the whole inventory.

### Examples
> profit
```
out: 2539.5
in: 79.72
profit: -2459.78
```
You can see what you have spend on your inventory and how much you earned by selling products.

> profit --date now
```
out: 2510.0
in: 46.92
profit: -2463.08
```

> profit --mindate 2021-06-01 --maxdate 2021-06-03
```
out: 21.0
in: 26.8
profit: 5.8
```

# today
When you want to see the current date, you use the action today
> today
```
2021-06-04
```

But with the following optional arguments you can change the date. Look out! if you change the date the program will use that date as current untill it is reset.
* --reset, when you changed the date you can reset it with this argument
* --setdate, you can choose the exact date you need for your report (yyyy-mm-dd)
* --setdays, you can choose how many days you want to go in the future (5), or in the past (-5)

### Examples

How to set a exact date:
> today --setdate 2021-04-01

> today
```
2021-04-01
```

How to set a date when you fill in the days you want to go in the future or past:

> today --setdays 1000

> today
```
2024-02-29
```

NOTE: because i did not reset the date to the current date, the action will count from the date set in the firts example (21-04-01)

Reset the date:
> today --reset

> today
```
2021-06-04
```

# help
To consult the help function use the following action:
> -h

A list of actions all and arguments will be shown
