# **User Story: Extracting Blog URL and Global-ID from Website_URL.csv**

## **Overview**
As a developer, I want to process a list of website URLs from `Website_URL.csv`, extract the blog URL from each website, and retrieve the **Global-ID** from the corresponding blog page. This will help automate the data collection process for better analysis and integration.

## **Acceptance Criteria**
1. The script should read `Website_URL.csv` and iterate through all the provided website URLs.
2. For each website, it should identify and extract the **Blog URL** (if available).
3. Once on the blog page, it should retrieve the **Global-ID** from the page content.
4. The extracted **Blog URL** and **Global-ID** should be stored in a structured format (e.g., CSV or JSON).
5. The script should handle errors gracefully, such as missing blog pages or inaccessible websites.