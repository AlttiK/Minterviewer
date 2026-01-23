chrome.tabs.onUpdated.addListener((tabID, changeInfo, tab) => {
    if (changeInfo.status == "complete" && tab.url && tab.url.includes("leetcode.com")) {
        chrome.scripting.executeScript({
            target: { tabId: tabID },
            files: ["content.js"]
        });
    }
});