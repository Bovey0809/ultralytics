# Linear Issues Fetcher for Depth Estimation

This guide explains how to fetch Linear issues related to depth estimation in the Ultralytics project.

## Quick Start

### 1. Get Your Linear API Key

1. Visit: https://linear.app/settings/api
2. Generate a new API key (requires Linear account access)
3. Copy the API key

### 2. Set Up Environment Variable

```bash
export LINEAR_API_KEY='lin_api_...'  # Replace with your actual key
```

### 3. Run the Script

```bash
# Search for "depth estimation" (default)
python3 show_linear_issues.py

# Search for custom terms
python3 show_linear_issues.py "MDE"
python3 show_linear_issues.py "monocular depth"
```

## Output

The script will display:
- Issue ID and identifier
- Title and description
- Current state (open, closed, etc.)
- Priority level
- Assignee and creator
- Labels
- Direct URL to the issue
- Creation and update timestamps

## Example Output

```
Found 5 issue(s) related to 'depth estimation':

--- Issue 1/5 ---
================================================================================
ID: ULT-123
Title: Implement depth estimation for YOLOv8
URL: https://linear.app/ultralytics/issue/ULT-123
State: In Progress (started)
Priority: High (1)
Team: ML Team (ML)
Assignee: John Doe
Labels: enhancement, depth-estimation
Created: 2025-01-15T10:30:00Z
Updated: 2025-01-20T14:22:00Z

Description:
--------------------------------------------------------------------------------
Add monocular depth estimation capabilities to YOLOv8 model...
================================================================================
```

## Troubleshooting

### No API Key Set

If you see: `Error: LINEAR_API_KEY environment variable not set`

Solution:
```bash
export LINEAR_API_KEY='your-api-key'
```

### No Issues Found

The script automatically tries alternative search terms:
- "depth"
- "MDE"
- "monocular depth"
- "depth_estimation"

### Authentication Error

If you get authentication errors:
1. Verify your API key is correct
2. Check that your Linear account has access to the workspace
3. Ensure the API key hasn't been revoked

## Advanced Usage

### Search Multiple Terms

```bash
# Create a shell script to search multiple terms
for term in "depth estimation" "MDE" "monocular" "KITTI"; do
    echo "=== Searching: $term ==="
    python3 show_linear_issues.py "$term"
done
```

### Save Results to File

```bash
python3 show_linear_issues.py > linear_issues.txt
```

### Filter by State

You can modify the script's GraphQL query to filter by specific states, priorities, or teams.

## Integration with Development Workflow

You can integrate this script into your development workflow:

1. **Pre-commit Hook**: Check for related issues before committing
2. **CI/CD Pipeline**: Verify issue status in automated workflows
3. **Daily Reports**: Generate issue summaries for the team

## Related Files

- `show_linear_issues.py` - Main script to fetch Linear issues
- `ultralytics/models/yolo/depth/` - Depth estimation implementation
- `ultralytics/models/yolo/depth/README.md` - MDE documentation
