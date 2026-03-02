# Presentation Script: Exception Monitoring Automation

## 1. Introduction (The Goal)
"Good morning everyone. Today, I want to show you a new tool we’ve built to help us stay ahead of technical issues. Think of it as a **smart alarm system** for our software. Its job is to watch over our production environment 24/7 and let us know the moment something unusual happens."

## 2. The Problem (The "Why")
"Right now, checking for errors can be slow and manual. It’s easy to miss a small issue before it becomes a big problem. We needed a way to automatically separate the 'normal' daily errors from 'new' or 'increasing' ones that actually need our attention."

## 3. Demo Cycle 1: The Instant Alert
**[DEMO CUE: Share the Web Interface and run Cycle 1]**

"I'll start with **Cycle 1**. This is the system's first look at the data. It immediately compares the current logs against our history. If it sees a **New** error that has never happened before, it doesn't wait—it alerts us instantly."

**[DEMO CUE: Switch to Microsoft Teams]**

"Here is the alert. Notice how it's marked as **'New'**. This tells the team they need to look at this right away because something changed in the environment."

## 4. Demo Cycle 2: The Verification Window
"But the system is smarter than just reacting to a single moment. It now enters **Cycle 2**."

**[DEMO CUE: Switch back to the Web Interface (explain the 30-min window)]**

"In a real scenario, the system waits for a 'Verification Window' (like 30 minutes). It then runs a second check. If the error count is still building up or a trend is confirmed, it sends a **Trending** alert."

**[DEMO CUE: Show the Cycle 2 result or Teams Trending alert]**

"This second alert is crucial. It confirms that this isn't just a temporary glitch—it’s a real problem that is **Elevated**. This helps us ignore the 'noise' and focus on the real signals."

## 5. The Value (The Bottom Line)
"By using this two-cycle approach, we get:
- **Faster Fixes**: We see new issues in minutes.
- **Accuracy**: The 30-minute verification ensures we don't get 'false alarms'.
- **Peace of Mind**: We know the system is being watched even when we aren't looking at the logs."

## 6. Closing
"The system is tested and ready. Our next step is to move from these manual runs to a fully live, continuous stream. Any questions?"
