# Sudoku Solver

## Introduction

This Python program implements a Sudoku Solver using depth-first search. The solver is designed to fill in a partially completed Sudoku board, adhering to the rules of Sudoku.

## SudokuState Class

The `SudokuState` class represents the state of the Sudoku board. It includes methods for initializing the board, adding numbers, removing conflicts, and finding the most constrained cell. The solver uses depth-first search to explore possible solutions.

## SudokuEntry Class

The `SudokuEntry` class represents a single entry in the Sudoku board. It includes methods for fixing a number, eliminating possibilities, and checking for conflicts.

## Usage

To run the Sudoku Solver, choose a problem configuration (e.g., `problem1()`, `problem2()`, or `heart()`), and execute the program. The solver will attempt to find a solution and display the final Sudoku board.
