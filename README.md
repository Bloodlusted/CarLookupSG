# Car Lookup SG
Simple Python program to retrieve the make/model and road tax expiry date of vehicles registered in Singapore from LTA's database.

They don't have an API for this (as far as I'm aware) so I am scraping their site.

## Instructions

You just need [Selenium](https://pypi.org/project/selenium/) to run the program.

```python
pip install selenium
```

Then, just run the program and enter the license plate of the vehicle you want to look up.

![Image](https://i.imgur.com/VEp5UhN.png)

*Note: This is a very early WIP and I will be improving it. The end goal is to deploy a web app.*