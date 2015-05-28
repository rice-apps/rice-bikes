Rice Bikes App TODO list
========================

- **Update models to reflect desired features**

  Question: How to define pk?

  See: /notes/model_notes

- **How to keep an electronic registry?**

  Idea: Add up on the fly? There won't be many orders, and then I can easily sort by date

- **How to choose services/products?**

  Idea: Hard-code the HTML with some jquery for expanding, pass back a unique string identifier ("drive_train", "43"), then have a back-end mapping ("drive-train" -> Service(name="Drive Train", price=10))

  - Question: Best way to make expandable divs?

  Idea: Separate service and customer (already done) and pass on the customer id to the service/part things, then submit the service/part forms with the customer id

  Question: Is wizard necessary/helpful? Is it restrictng me?

  Question: Can I reuse forms and associated views for both out- and in-patient?

  - Idea: Pass something to tell whether it's in- or out- patient, then define where to go next based on that

- **Add more details to emails/separate pick-up emails and receipts**

- **Send any updates to customer?** **** ask brian

- **Research how to make some fields' optionality dependent upon others' values**