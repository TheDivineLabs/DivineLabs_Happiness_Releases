---
title: Startup recovery and in-app updates
date: 2026-11-04
version: 0.2.12-dev
source_sha256: d5eeaebdb6ad6ef1579c51738fadd0913e42fc838a0d2908dd851e0d277cd12c
---
A local build now includes a recovery window with the failure reason, retry, a separate clean profile and a support report. If the embedded page crashes, the client offers to reload the game.

Updates can be checked inside the application. Downloads require confirmation, and installation preserves settings and profiles. Startup checks can be disabled.

The public installer and portable download have not been updated yet. Online updating requires compatible files to be published in a release.
