# Practice Math - the Python Edition

A site for kids to practice their math.

Initially I was going to load a series of equations into the site and randomly present them to users. This would obviously involve a fair amount of work but, you know, it would have been for our children.

It then occurred to me that I could randomly generate values and populate pre-defined fields to create equations. Kids could then type in their answers, and have the system evaluate their answers based on the current values.

The site should also keep track of how the kids do in their session and give them a way to review their work.

## Functionality I'm aiming for

Here is an overview of what I have in mind:

![Rough overview of the app](http://cld.wthms.co/yLuGDh+)

I'm aiming for the following functionality:

1. Randomly calculated number values and an operator;
2. Give the user a way to choose the maximum values that can be generated;
3. Add a means for a user to also specify which operators they want to work with (younger kids may not be ready for multiplication and division, for example);
4. Create equations using randomly generated values and a math operator;
5. Represent fractions in the web interface using some sort of LaTeX integration;
6. Calculate the solution of the equation, as it's generated each time, and compare the user's answer to the actual solution;
7. Give feedback to the user dependng on whether the answer was correct;
8. Keep track of the user's score as they go;
9. Provide a user-friendly web interface including "Submit", "Next", and "Finish" buttons;
10. When the user clicks on the "Finish" button, a list of completed equations and responses will be presented below (along with feedback on which ones were answered correctly).

## Constraints

I've added one key constraint for now. Because our kids don't do equations with negative values as results, I've added this basic logic that forces the script to generate a new equation is the solution is less than zero:

```
if solution > 0:
        return solution
    else:
        gen_equations()
```

