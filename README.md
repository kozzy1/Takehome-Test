# Takehome-Test

Request:

{
  "images": [
    "http://example.com/image1",
    "http://example.com/image2",
    "http://badurl.com/image3",
  ]
}

Success Response:

{
  "results": [
    {
      "url": "http://example.com/image1",
      "classes": [
        {
          "class": "person",
          "confidence": 0.8641
        },
        {
          "class": "dog",
          "confidence": 0.00516
        }
      ]
    },
    {
      "url": "http://example.com/image2",
      "classes": [
        {
          "class": "cat",
          "confidence": 0.2115
        }
      ]
    },
    {
      "url": "http://example.badurl.com/image3",
      "error": "Invalid URL"
    }
  ]
}
