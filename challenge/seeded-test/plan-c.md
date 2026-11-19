## Brief
- Goal: Captains can register a team for my one-day 5-a-side tournament on a web page, registration stops at exactly 16 teams, and I get the final list of teams and captain contacts.
- Constraints: I am the only organiser and developer. Free hosting tier. A small Python Flask app with a SQLite database. The tournament is on Saturday 13 June 2026. Fees are paid in cash on the day.
- Non-goals: No online payment. No user accounts for captains. No live scores or brackets on the site.

## Plan
1. One public page with a form: team name, captain name, captain email, captain phone. Below the form, the list of team names registered so far.
2. Submitting the form sends the data to the server, which saves every submission it receives as a new row in the `teams` table and reloads the page.
3. The page counts the listed teams. When 16 are listed, the page hides the form and shows "Tournament full".
4. An organiser page at `/organiser-list` shows the full table with captain names, emails and phone numbers. It has no login; I keep the link unlisted and bookmark it.
5. Registration closes on Friday 12 June 2026 at 18:00. After that time the public page shows "Registration closed" instead of the form.
6. On Thursday 11 June I build the match schedule from the final list of teams and email it to all captains.
7. Back up the database file to my PC once a day by downloading it from the host's file browser.
8. Test before sharing the link: register 3 test teams from my phone and my PC, check they appear in both lists, then clear the table.
9. Share the link in the league's group chat on Monday 25 May.
10. Done when registration has closed, the organiser page shows at most 16 teams, and every captain has received the schedule.

## Risks I already know about
- The free hosting tier may be slow to wake up on the first visit.
- A captain may mistype their email address and not receive the schedule.
- Teams may drop out after registering, leaving an uneven number.
