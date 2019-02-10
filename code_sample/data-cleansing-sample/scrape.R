# scrape profiles for one fruit from ndb.nal.usda.gov

if (!require("rvest")) install.packages("rvest")
library("rvest")

scrape_fiber = function(food_name) {
    # step a: request ndb website
    url0 = paste0("https://ndb.nal.usda.gov/ndb/search/list?",
                  "list&qt=&ds=Standard+Reference&qlookup=")
    url = paste0(url0, food_name)  first_html = try(read_html(url), silent=TRUE)
    if (is(first_html, "try-error")){
        stop ("There is no match")
    }
    
    # step b: get alert text
    alert_text = html_text(html_nodes(first_html, "div.alert"))
    alert_text = trimws(alert_text)
    alert_no = strsplit(alert_text, " ")[[1]][1]
    if (length(alert_text) == 0 || alert_no == 'No'){
        return ("error: -1 food not found")
    }
    cat(alert_text)
    
    # step c: get "fruit, raw" URL and open it
    td_nodes = html_nodes(first_html, "td")
    raw_idx = grep(", raw", td_nodes)[1]
    if (length(raw_idx) == 0 || is.na(raw_idx)){
        return ("error: -2 food does not have a raw form")
    }
    
    raw_node = td_nodes[raw_idx]
    raw_url = html_attr(html_nodes(raw_node, "a"), "href")
    fruit_url = paste0("http://ndb.nal.usda.gov", raw_url)
    download.file(fruit_url, destfile = "scrapedpage.html", quiet=TRUE)
    html_new = read_html(url(fruit_url))
    
    # step d:
    table_data = html_nodes(html_new, "table#nutdata")
    if (length(table_data) == 0){
        return ("-3: 'nutdata' table not found")
    }
    table = html_nodes(table_data, "td")
    fiber_idx = grep("Fiber, total dietary", table)+2
    if (length(fiber_idx) == 0){
        return ("-4: 'Fiber, total dietary' row header not found")
    }
    
    fiber = table[fiber_idx]
    fiber_text = html_text(fiber)
    return(suppressWarnings(as.numeric(fiber_text)))
}
