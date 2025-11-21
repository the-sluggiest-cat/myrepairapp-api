.. MyRepairApp.py documentation master file, created by
   sphinx-quickstart on Wed Nov 19 14:22:36 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MyRepairApp.py
==============

A Python wrapper for MyRepairApp that uses their `public API <https://www.myrepairapp.com/api-docs/public-api>`_.

Very little assistance provided by Gemini for code suggestions. 99.8% of the codebase was written by humans.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

..
   # MyRepairApp.py

   A Python wrapper for MyRepairApp that uses their [public API](https://www.myrepairapp.com/api-docs/public-api).

   Very little assistance provided by Gemini for code suggestions. 99.8% of the codebase was written by humans.

   ## Examples:

   ```py
   import myrepairapp.api

   mrp = myrepairapp.api.MyRepairApp("insert-api-key-here")

   print(mrp.inventory_search("iPhone"))
   ```

   This returns a list of `InventoryItem`s that can be combed through for customer data (name, phone number, e-mail) and the like.

   ## To use:

   You need to provide your own API key, which can be found [here](https://www.myrepairapp.com/api-access), when signed into a business that uses MyRepairApp.

   Keep in mind all functions are **blocking in nature**. Asynchronous work is WIP.


