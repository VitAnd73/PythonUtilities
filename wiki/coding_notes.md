# #XPATH

Getting attributes of elements and other attributes/methods: - [https://lxml.de/api/lxml.etree.\_Element-class.html](https://lxml.de/api/lxml.etree._Element-class.html)
Done via "eval" of the code that is provided after the splitter = "&&" - use HTML element (object) "e" or function deCFEmail (for handling hidden email addresses like in [Cloudflare](https://stackoverflow.com/questions/58103525/how-to-decode-email-xa0protected-while-web-scraping-using-python))
    getting text:
        e.text\_content() - <span class="colour" style="color:rgb(64, 64, 64)">Return the text content of the tag (and the text in any children)</span>
        e.text - <span class="colour" style="color:rgb(0, 0, 0)">Text before the first subelement. This is either a string or the value None, if there was no text.</span>
    getting attributes (like src, href, etc.)
        e.get('src')
        e.get('href')
    getting hidden email (executing function deCFEmail)
        deCFEmail(e.get('data-cfemail'))

<br>
example of command to run:
"C:\0\_sber\housing\mcs\_2\_2.csv" --outfilepath "C:\0\_sber\housing\mcs\_2\_2\_res.csv"

<br>
# Selenium

[https://www.geeksforgeeks.org/how-to-install-selenium-in-python/](https://www.geeksforgeeks.org/how-to-install-selenium-in-python/)