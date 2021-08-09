# Company Info in Ecuador

In principle, basic information about all companies in Ecuador is a matter of public record.  The "Superintendent of Companies" is required to make the data available online, so that anyone can use it.  However, they didn't make it available as a file that anyone can download - instead, you must search for the specific name of the company that you're interested in.  This isn't terribly useful for academics, journalists, etc.

However, each company has a unique (and sequential) record ID.  So I simply iterate over the full range of IDs, saving the results for each one.  There were fewer than 190k records, so even scraping very politely (less than one request per second), this took less than a week to run.  The errors could have been handled more gracefully, but since this was a one-off project, I just reran the script later looking for any missed results.


