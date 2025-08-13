# ==============================================================================
# Code Crawler: Ignore Patterns (`config.py`)
# ==============================================================================
#
# This file defines the `ignore_patterns` list, which controls which files and
# directories are excluded from the analysis.
#
# HOW IT WORKS:
# The list is imported by `analyzer.py` and used to filter the file paths
# during the directory walk. The patterns are simple glob-style strings that
# are matched against paths relative to the project root (where the crawler
# is executed).
#
# ==============================================================================
# Crawler Configuration
# ==============================================================================
# This file specifies directories and files to be ignored by the code crawler.
# The matching logic is inspired by how `.gitignore` works.
#
# HOW TO USE:
# - Add glob patterns to the `ignore_patterns` list.
# - Patterns are matched against paths relative to the project root.
#
# PATTERN RULES:
#
# 1. To ignore a directory and all its contents, add a trailing slash.
#    - `'my_dir/'` ignores the entire directory.
#
# 2. To ignore files by a pattern everywhere, do not use a slash.
#    - `'*.log'` ignores all log files.
#    - `'__pycache__'` ignores all __pycache__ directories.
#
# 3. To ignore a specific file or path, use the full relative path.
#    - `'AdvancedMath/main.py'` ignores only that specific file.
#
# IMPORTANT: The recursive wildcard `**` is NOT supported. Blank lines and
# lines starting with '#' are ignored.
# ==============================================================================

# config.py
ignore_patterns = [
    # General file patterns (no slash)
    '*.pyc',
    '*.DS_Store',
    '*.png',
    '*.jpg',
    '*.jpeg',
    '*.gif',
    '*.log',
    'ENHANCEMENTS.md',
    'FUM_Novelty_Memo.md',
    'MESSAGE_TO_ROO.txt',

    # General directory patterns (no slash)
    '.git',
    '__pycache__',
    
    # Path-specific directory patterns (must end with /)
    'ignore/',
    '.vscode/',
    'venv/',
    'code_crawler/',
    #'FullyUnifiedModel/',
    'MIGRATE_PENDING_fum_rt/',
    'from_physicist_agent/',
    'CURRENT_PLAN/',
    'data/',
    'fum_rt/data/',
    '_FUM_Training/',
    'mathematical_frameworks/',
    'planning_outlines/',
    'code_crawler_results/',
    'FullyUnifiedModel/How_The_FUM_Works/Reference_Assets/Audio-Docs/',
    'runs/benchmark_1/',
    'runs/demo_1/',
    'runs/run_1752954844/',
    'runs/run_1752958459/',
    'runs/run_1752959364/',
    'fum_rt/fum_advanced_math/causal_inference/',
    'fum_rt/fum_advanced_math/clustering/',
    'fum_rt/fum_advanced_math/dynamical_systems/',
    'fum_rt/fum_advanced_math/evolutionary/',
    'fum_rt/fum_advanced_math/fractal_analysis/',
    'fum_rt/fum_advanced_math/fractional_calculus/',
    'fum_rt/fum_advanced_math/graph/',
    'fum_rt/fum_advanced_math/iit/',
    'fum_rt/fum_advanced_math/info_theory/',
    'fum_rt/fum_advanced_math/neuro/',
    'fum_rt/fum_advanced_math/optimization/',
    'fum_rt/fum_advanced_math/ot/',
    'fum_rt/fum_advanced_math/pathway_analysis/',
    'fum_rt/fum_advanced_math/rmt/',
    'fum_rt/fum_advanced_math/sde/',
    'fum_rt/fum_advanced_math/semantic/',
    'fum_rt/fum_advanced_math/soc_analysis/',
    'fum_rt/fum_advanced_math/spatial/',
    'fum_rt/fum_advanced_math/stochastic/',
    'fum_rt/fum_advanced_math/structural_plasticity/',
    'fum_rt/fum_advanced_math/symbolic/',
    'fum_rt/fum_advanced_math/tda/',
    'fum_rt/fum_advanced_math/thermodynamics/',
    'fum_rt/fum_advanced_math/time_series/',
    'fum_rt/fum_advanced_math/void_dynamics/',
    'fum_rt/fum_advanced_math/calculate_descriptive_stats.py',
    'fum_rt/fum_advanced_math/linear_system_solver.py',
    'fum_rt/fum_advanced_math/numerical_integrate.py',
    'fum_rt/fum_advanced_math/numerical_ode_solver.py',
    'fum_rt/fum_advanced_math/symbolic_differentiation.py',
    'AdvancedMath/causal_inference/',
    'AdvancedMath/clustering/',
    'AdvancedMath/dynamical_systems/',
    'AdvancedMath/evolutionary/',
    'AdvancedMath/fractal_analysis/',
    'AdvancedMath/fractional_calculus/',
    'AdvancedMath/graph/',
    'AdvancedMath/iit/',
    'AdvancedMath/info_theory/',
    'AdvancedMath/optimization/',
    'AdvancedMath/ot/',
    'AdvancedMath/pathway_analysis/',
    'AdvancedMath/rmt/',
    'AdvancedMath/sde/',
    'AdvancedMath/semantic/',
    'AdvancedMath/soc_analysis/',
    'AdvancedMath/spatial/',
    'AdvancedMath/stochastic/',
    'AdvancedMath/symbolic/',
    'AdvancedMath/thermodynamics/',
    'AdvancedMath/time_series/',

    # # Path-specific file patterns
    'AdvancedMath/calculate_descriptive_stats.py',
    'AdvancedMath/linear_system_solver.py',
    'AdvancedMath/numerical_integrate.py',
    'AdvancedMath/numerical_ode_solver.py',
    'AdvancedMath/symbolic_differentiation.py',
]