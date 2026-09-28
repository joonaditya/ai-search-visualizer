# Project 1 Report: Intelligent Search Visualizer

> [!IMPORTANT]
> **AUTOGRADER COMPLIANCE INSTRUCTIONS:**
> This report is parsed automatically by the autograder. To ensure you receive full credit for your work:
> 1. **Do not modify** the section headers (`## ...`) or bold field keys (e.g., `**Name:**`, `**Selected Region:**`, `**Live Deployment URL:**`, etc.).
> 2. **Write your answers directly after** the colon `:` of each field, replacing the placeholder text completely (including the outer brackets `[` and `]`).
> 3. **Maintain the file structure**. Changing headers, bold titles, or deleting lines can cause the autograder to miss your responses and award 0 marks.

---

## Student Information 
- **Name:** Aditya Lnu
- **UID (netID):** alnu55
- **UIN:** 663683641

---

## Section 1: Selected City Region
- **Selected Region:** Chicago

---

## Section 2: Map Graph Configuration
- **Total Cities Configured:** 22
- **Total Connection Edges:** 30
- **Graph Fully Connected:** Yes

---

## Section 3: Local Verification & Search Algorithms
*Check the algorithms you successfully ran and verified on your local development server by placing an `x` in the brackets (e.g., `[x]`):*
- [X] Breadth-First Search (BFS)
- [X] Depth-First Search (DFS)
- [X] Uniform Cost Search (UCS)
- [X] Iterative Deepening Search (IDS)
- [X] Greedy Best-First Search (Greedy)
- [X] A* Search (A*)

---

## Section 4: Deployed and Presentation Information
- **Deployment Platform:** Render
- **Live Deployment URL:** https://ai-search-visualizer-lv40.onrender.com/
- **Video Presentation Link:** https://drive.google.com/drive/folders/13vnz9e5jkwf5a_KHqcoN4sGsnHMPdlaG?usp=sharing

---

## Section 5: Discussion
- **Which search algorithm is best for this route finding problem?** 
    A* was the best algorithm. It consistently found the optimal route while expanding relatively fewer nodes and it also produced the most optimal cost.
    Greedy expanded the fewest nodes in many cases but its cost was very high.
- **Search Efficiency (Nodes expanded/time taken comparison):**
    Greedy Best-First search: expanded fewest nodes, but routes were not always optimal.
    A* expanded few nodes, while optimal running costs.
    BFS was fast and expanded moderate number of notes, but because of weighted edges it wasnt always the cheapest route.
    UCS found optimal routes consistently but required more nodes and time as compares to BFS or A*
    DFS was often very fast and expanded relatively fewre nodes too but its solution quality was incosistent.
- **Link the idea of search algorithm to today Generative AI.** 
    They are similar because they both search through many possible choices to find a good solution. These algorithms use different paths to find a solution while Gen AI looks at different possible sequences of tokens when producing an answer. The main difference is that these search algorithms use defined states, costs and rules while Generative AI uses learned models to estimate the solution. 
