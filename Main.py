import random
import string
import time

# Function to evaluate the strength of the password
def evaluate_password_strength(password):
    """
    Evaluates the strength of the password.
    - Weak: Less than 8 characters.
    - Medium: Between 8 and 12 characters.
    - Strong: 12 or more characters.
    """
    length = len(password)
    if length < 8:
        return 'Weak'
    elif 8 <= length <= 12:
        return 'Medium'
    else:
        return 'Strong'

# Function to suggest improvements based on the current password
def suggest_improvements(password):
    """
    Suggests improvements if the password is not strong.
    - Add length, numbers, uppercase letters, lowercase letters, and special characters.
    """
    improvements = []
    if len(password) < 12:
        improvements.append("Increase the length of your password.")
    if not any(char.isdigit() for char in password):
        improvements.append("Include at least one number.")
    if not any(char.isupper() for char in password):
        improvements.append("Include at least one uppercase letter.")
    if not any(char.islower() for char in password):
        improvements.append("Include at least one lowercase letter.")
    if not any(char in string.punctuation for char in password):
        improvements.append("Include at least one special character.")
    return improvements

# Function to generate 5 strong passwords based on the original password
def generate_strong_passwords_from_original(original_password):
    """
    Generates 5 strong passwords based on the original password.
    It improves the password by adding missing character types.
    """
    strong_passwords = []
    
    # Improve the original password by making sure it has a good mix of characters
    for _ in range(5):
        password = list(original_password)
        
        # Add missing character types if necessary
        if not any(char.isupper() for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.ascii_uppercase)
        if not any(char.islower() for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.ascii_lowercase)
        if not any(char.isdigit() for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.digits)
        if not any(char in string.punctuation for char in password):
            password[random.randint(0, len(password) - 1)] = random.choice(string.punctuation)
        
        # Ensure the password is long enough (12 characters)
        while len(password) < 12:
            password.append(random.choice(string.ascii_letters + string.digits + string.punctuation))
        
        # Shuffle the characters to make it more random
        random.shuffle(password)
        
        # Convert list back to string
        strong_passwords.append("".join(password))
    
    return strong_passwords

# Genetic algorithm for password guessing
def genetic_algorithm(password):
    """
    Uses genetic algorithm to guess the password based on the input.
    The algorithm will try to match the user password by evolving the population.
    """
    start_time = time.time()
    
    # Population size and number of generations
    population_size = 100
    generations = 1000
    mutation_rate = 0.1
    target = password
    
    # Generate initial population
    population = [''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=len(target))) for _ in range(population_size)]
    
    # Fitness function to rank individuals in population
    def fitness(individual):
        return sum([1 if individual[i] == target[i] else 0 for i in range(len(target))])

    # Run the genetic algorithm
    for generation in range(generations):
        population = sorted(population, key=lambda x: -fitness(x))
        if fitness(population[0]) == len(target):
            break  # Stop if a perfect match is found
        
        new_population = population[:10]  # Keep the best 10 individuals
        
        # Mutate and crossover to generate new individuals
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(population[:50], k=2)
            crossover_point = random.randint(0, len(target))
            child = parent1[:crossover_point] + parent2[crossover_point:]
            
            # Mutation
            if random.random() < mutation_rate:
                child = mutate_password(child)
            
            new_population.append(child)
        
        population = new_population
    
    elapsed_time = time.time() - start_time
    best_password = population[0]
    password_strength = evaluate_password_strength(best_password)
    improvements = suggest_improvements(best_password) if password_strength != 'Strong' else []
    
    # Generate strong password suggestions based on the original password if it's not strong
    strong_passwords = generate_strong_passwords_from_original(password) if password_strength != 'Strong' else []
    
    return best_password, password_strength, elapsed_time, improvements, strong_passwords

# Function to mutate the password
def mutate_password(password):
    """
    Mutates the password by randomly changing one character.
    """
    password = list(password)
    index = random.randint(0, len(password) - 1)
    new_char = random.choice(string.ascii_letters + string.digits + string.punctuation)
    password[index] = new_char
    return ''.join(password)

# Main function
def main():
    # Prompt user to input password
    user_password = input("Enter your password: ")
    
    # Run the genetic algorithm to guess the password
    best_password, password_strength, elapsed_time, improvements, strong_passwords = genetic_algorithm(user_password)
    
    # Display results
    print("\nBest password found:", best_password)
    print("Password strength:", password_strength)
    print(f"Time taken to guess the password: {elapsed_time:.2f} seconds")
    
    # Only display improvements and suggestions if the password is not strong
    if password_strength != 'Strong':
        print("\nSuggested improvements for your password:")
        for improvement in improvements:
            print(f"- {improvement}")
        
        # Display 5 strong password suggestions based on the original password
        print("\nHere are 5 strong password suggestions based on your original password:")
        for i, strong_password in enumerate(strong_passwords, start=1):
            print(f"Suggestion {i}: {strong_password}")

# Run the program
if __name__ == "__main__":
    main()
