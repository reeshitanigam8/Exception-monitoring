# Video Script: Exception Monitoring Automation

## Part 1: The Manual Process (Background)
**[Visual: Face to camera or a slide showing "The Before"]**

"Hi everyone. Today I'm going to walk you through our new Exception Monitoring Automation. But before we dive into the tool, let's talk about why we built it."

"Previously, our team had a very manual process. Every day, someone had to:
1. Log into Dynatrace.
2. Manually export the exception data.
3. Open a massive Excel sheet and compare hundreds of rows to see what was new or what had increased.
4. If they found something, they had to manually notify the right people."

"This was time-consuming, and because it was manual, it was easy for a critical issue to stay hidden in the noise for hours."

## Part 2: The Solution & Web Interface
**[Visual: Share your screen showing the Web Interface]**

"To solve this, we created this **Exception Monitoring Portal**. It’s a simple, web-based interface that handles the entire workflow for us. It acts like a smart filter for our system's health."

"Let me show you how it works in practice."

## Part 3: Cycle 1 - The Instant Alert
**[Visual: Show yourself uploading a CSV or clicking 'Run' for Cycle 1]**

"We start with **Cycle 1**. As soon as the data is uploaded, the automation immediately compares it against our production baseline. It’s looking for 'New' exceptions—things our system has never seen before."

**[Visual: Switch to Microsoft Teams and show the 'New' alert]**

"And here is the result. Within seconds, the team gets a clear notification in Microsoft Teams. It tells us exactly what the error is and where it's happening. No more digging through spreadsheets—the alert comes to us."

## Part 4: Cycle 2 - Verification & Trending
**[Visual: Switch back to the Web Interface]**

"But we don't just want alerts for every tiny spike. That’s where **Cycle 2** comes in. Following a 30-minute verification window, the system runs again."

**[Visual: Show Cycle 2 running or the result]**

"It checks if the error is still there or if the count is increasing. If it confirms a trend, it sends a **Trending** or **Elevated** alert. This ensures we focus our energy on real, persistent problems rather than temporary glitches."

## Part 5: Future Roadmap - Full Automation
**[Visual: Face to camera or a slide showing "Next Steps"]**

"Right now, the tool is a huge leap forward. But we’ve designed it with the future in mind. 

Currently, we are using file uploads to feed the system. However, if we get access to the **Dynatrace API**, we can automate this entire process end-to-end. The system will be able to 'pull' the data itself directly from Dynatrace every few minutes, making it a completely hands-off, 24/7 monitoring solution."

## Part 6: Summary & Closing
"In summary, this automation moves us from a reactive, manual process to a proactive, intelligent one. We get:
- **Instant visibility** into new issues.
- **Trend verification** to reduce noise.
- And a **clear path** to full automation."

"Thanks for watching, and I'm happy to dive deeper into any of these features!"
