### Iterative Development

#### Checklist

- Mock ups
- Routing
- Templates and Forms
- CRUD Functionality
    - url_for
    - redirects 
    - GET & POST requests
- API Endpoints
- Styling and Message Flashing


#### Restaurant Layout

URL Routing | Method | Message
---- | ----------- | ------------
/ <br>/restaurants | showRestaurants()  | This page will show all restaurants
/restaurantnew | newRestaurant() | This page will enable user to add new restaurant
/restaurant/restaurant_id/edit | editRestaurant()  | Enable user to edit restaurant name
/restaurant/restaurant_id/delete |  deleteRestaurant() | Enable user to delete restaurant
/restaurant/restaurant_id <br> /restaurant/restaurant_id/menu  |  showMenu() | Display restaurant’s menu
/restaurant/restaurant_id/menu/new | newMenutItem() | Add a new menu item
/restaurant/restaurant_id/menu/menu_id/edit | editMenuItem() | Edit a specific menu item
/restaurant/restaurant_id/menu/menu_id/delete | deleteMenuItem() |  Delete a specific menu item

<hr />

**Top-Down versus Bottom-Up** \* Algorithm Design

Basis for comparison | Top-down Approach | Bottom-up Approach
--------------------------- | ----------------------------- | ------------------------------
Basic | Breaks the massive problem into smaller subproblems. | Solves the fundamental low-level problem and integrates them into a larger one.
Process | Submodules are solitarily anaylsed | Examine what data is to be encapsulated, and implies the concept of information hiding.
Communication | Not required in top-down approach | Needs a specific amount of communication
Redundancy | Contain redundant info | Redundancy can be eliminated
Programming Languages | Structure/procedural oriented programming languages (i.e. C) follows the top-down approach | Object-oriented programming languages (like C++, Java, etc.) follows the bottom-up approach.
Mainly Used In | Module documentation, test case creation, code implementation and debugging | Testing

\* Website [Reference](https://techdifferences.com/difference-between-top-down-and-bottom-up-approach.html)
