# Chuwa Training

Assignment submission repo. Put coding homework under `Coding/` and short-answer questions under `ShortQuestions/`.

```
.
├── Coding/           # coding assignments (e.g. Coding/hw1/...)
└── ShortQuestions/   # written answers (e.g. ShortQuestions/hw1.md)
```

## How to submit your assignments using this repo

### Step 1: Fork this repo

Students **must fork** this repository to their own GitHub account first.

Click **Fork** on the top-right corner of this repo.

### Step 2: Clone *your forked repo*

```bash
cd your_work_dir
git clone https://github.com/<your_github_username>/chuwa92126.git
cd chuwa92126
```

(Optional but recommended) Add the original repo as upstream:

```bash
git remote add upstream https://github.com/KKKTT-cyk/chuwa92126.git
```

### Step 3: Create your own master branch

Create a personal master branch in your fork:

```bash
git checkout -b firstName_lastName/master
git push origin firstName_lastName/master
```

### Step 4: Create a homework feature branch

For each homework, create a new branch from your own master branch:

```bash
git checkout firstName_lastName/master
git checkout -b firstName_lastName/hw1
```

> **Branch names matter.** The submissions table below is generated automatically from the branch name,
> so it must be `firstName_lastName/hwN` (e.g. `tingyu_chang/hw3`). Other names may not be counted.

Work on your assignment, then commit and push:

```bash
git add .
git commit -m "Finish HW1"
git push origin firstName_lastName/hw1
```

### Step 5: Raise a Pull Request (PR)

1. Go to your fork on GitHub.
2. Click **Compare & pull request** (or **Pull requests → New pull request**).
3. Set the branches:
   - **base repository**: `KKKTT-cyk/chuwa92126`, **base**: `main`
   - **head repository**: `<your_github_username>/chuwa92126`, **compare**: `firstName_lastName/hw1`
4. Title the PR `firstName_lastName hw1` and click **Create pull request**.

## HW Submissions

Updated automatically by [`.github/workflows/submissions.yml`](.github/workflows/submissions.yml) whenever a PR is opened, closed or edited. Do not edit this table by hand.

<!-- SUBMISSIONS:START -->
| GitHub | Student Name | HW | PR Status | Submitted At | PR URL |
|--------|--------------|----|-----------|--------------|--------|
| tiffiong | Tiffany Iong | hw1 | open | 2026-09-23 14:04:37 | [link](https://github.com/KKKTT-cyk/chuwa92126/pull/1) |
<!-- SUBMISSIONS:END -->
