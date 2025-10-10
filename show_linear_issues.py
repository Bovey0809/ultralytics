#!/usr/bin/env python3
# Ultralytics 🚀 AGPL-3.0 License - https://ultralytics.com/license
"""
Script to fetch Linear issues related to depth estimation.

Requires LINEAR_API_KEY environment variable to be set.
"""

import json
import os
import sys
from typing import Any

try:
    import requests
except ImportError:
    print("Error: requests library not found. Installing...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests


LINEAR_API_URL = "https://api.linear.app/graphql"


def get_linear_issues(api_key: str, search_term: str = "depth estimation") -> list[dict[str, Any]]:
    """
    Fetch Linear issues related to a search term.

    Args:
        api_key: Linear API key
        search_term: Term to search for in issues

    Returns:
        List of issues matching the search term
    """
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

    # GraphQL query to search for issues
    query = """
    query SearchIssues($searchTerm: String!) {
      issues(
        filter: {
          or: [
            { title: { containsIgnoreCase: $searchTerm } }
            { description: { containsIgnoreCase: $searchTerm } }
          ]
        }
        first: 50
      ) {
        nodes {
          id
          identifier
          title
          description
          state {
            name
            type
          }
          priority
          priorityLabel
          assignee {
            name
            email
          }
          creator {
            name
            email
          }
          team {
            name
            key
          }
          labels {
            nodes {
              name
              color
            }
          }
          url
          createdAt
          updatedAt
        }
      }
    }
    """

    variables = {"searchTerm": search_term}

    try:
        response = requests.post(
            LINEAR_API_URL, headers=headers, json={"query": query, "variables": variables}, timeout=30
        )
        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            print(f"GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
            return []

        return data.get("data", {}).get("issues", {}).get("nodes", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching Linear issues: {e}")
        return []


def format_issue(issue: dict[str, Any]) -> str:
    """Format a Linear issue for display."""
    lines = []
    lines.append("=" * 80)
    lines.append(f"ID: {issue['identifier']}")
    lines.append(f"Title: {issue['title']}")
    lines.append(f"URL: {issue['url']}")
    lines.append(f"State: {issue['state']['name']} ({issue['state']['type']})")

    if issue.get("priority"):
        lines.append(f"Priority: {issue['priorityLabel']} ({issue['priority']})")

    if issue.get("team"):
        lines.append(f"Team: {issue['team']['name']} ({issue['team']['key']})")

    if issue.get("assignee"):
        lines.append(f"Assignee: {issue['assignee']['name']}")

    if issue.get("creator"):
        lines.append(f"Creator: {issue['creator']['name']}")

    if issue.get("labels", {}).get("nodes"):
        labels = [f"{label['name']}" for label in issue["labels"]["nodes"]]
        lines.append(f"Labels: {', '.join(labels)}")

    lines.append(f"Created: {issue['createdAt']}")
    lines.append(f"Updated: {issue['updatedAt']}")

    if issue.get("description"):
        lines.append("\nDescription:")
        lines.append("-" * 80)
        # Truncate long descriptions
        desc = issue["description"]
        if len(desc) > 500:
            desc = desc[:500] + "..."
        lines.append(desc)

    lines.append("=" * 80)
    return "\n".join(lines)


def main():
    """Main function to fetch and display Linear issues."""
    # Get API key from environment
    api_key = os.getenv("LINEAR_API_KEY")

    if not api_key:
        print("Error: LINEAR_API_KEY environment variable not set.")
        print("\nTo use this script:")
        print("1. Get your Linear API key from: https://linear.app/settings/api")
        print("2. Set the environment variable:")
        print("   export LINEAR_API_KEY='your-api-key-here'")
        print("3. Run this script again")
        sys.exit(1)

    # Allow custom search term via command line argument
    search_term = sys.argv[1] if len(sys.argv) > 1 else "depth estimation"

    print(f"Searching Linear for issues related to: '{search_term}'")
    print("-" * 80)

    # Fetch issues
    issues = get_linear_issues(api_key, search_term)

    if not issues:
        print(f"\nNo issues found matching '{search_term}'")
        print("\nTrying alternative searches...")

        # Try alternative search terms
        alternatives = ["depth", "MDE", "monocular depth", "depth_estimation"]
        for alt_term in alternatives:
            if alt_term == search_term:
                continue
            print(f"\nSearching for: '{alt_term}'")
            issues = get_linear_issues(api_key, alt_term)
            if issues:
                search_term = alt_term
                break

    if not issues:
        print("\nNo issues found with any depth-related search terms.")
        return

    # Display results
    print(f"\nFound {len(issues)} issue(s) related to '{search_term}':\n")

    for i, issue in enumerate(issues, 1):
        print(f"\n--- Issue {i}/{len(issues)} ---")
        print(format_issue(issue))

    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total issues found: {len(issues)}")

    # Group by state
    states = {}
    for issue in issues:
        state = issue["state"]["name"]
        states[state] = states.get(state, 0) + 1

    print("\nBy State:")
    for state, count in sorted(states.items()):
        print(f"  {state}: {count}")

    # Group by priority
    priorities = {}
    for issue in issues:
        priority = issue.get("priorityLabel", "None")
        priorities[priority] = priorities.get(priority, 0) + 1

    if any(p != "None" for p in priorities.keys()):
        print("\nBy Priority:")
        for priority, count in sorted(priorities.items()):
            print(f"  {priority}: {count}")


if __name__ == "__main__":
    main()
