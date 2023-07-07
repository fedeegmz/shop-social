# Shop-Social
In our platform you can find a lot of shops. It contains products and you can buy them.  

## Endpoints  
### users
- GET: **/users** -> show all users
- GET: **/users/<username>** -> show a user with username
- POST: **/users/signup** -> register a user
### login
- POST: **/login/token** -> login with username and password. Get an access_token
- GET: **/login/users/me** -> show my data
### shops
- GET: **shops** -> show all shops
- GET: **/shops/<shop_name>** -> show a shop with its name
- POST: **/shops** -> register a shop
- POST: **/shops/<shop_name>/insert-product** -> register a product in a shop
- POST: **/shops/<shop_name>/<product_id>/update-stock/<stock>** -> update the stock of a product
- POST: **/shops/<shop_name>/<product_id>/add-to-cart** -> add a product in the cart