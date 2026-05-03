# Module 8 Assignment: Data Lookup with Dictionaries & Basic Aggregation
# GlobalTech Solutions Customer Management System

print("=" * 60)
print("GLOBALTECH SOLUTIONS - CUSTOMER MANAGEMENT SYSTEM")
print("=" * 60)

# TODO 1: Service categories
services = {
    "Web Development": 150,
    "Data Analysis": 175,
    "Cybersecurity": 220,
    "Cloud Consulting": 200,
    "IT Support": 90
}

# TODO 2: Customer dictionaries
customer1 = {
    "company_name": "Alpha Corp",
    "contact_person": "John Smith",
    "email": "john@alphacorp.com",
    "phone": "555-1234"
}

customer2 = {
    "company_name": "Beta Solutions",
    "contact_person": "Lisa Brown",
    "email": "lisa@betasolutions.com",
    "phone": "555-2345"
}

customer3 = {
    "company_name": "Gamma Industries",
    "contact_person": "Mike Johnson",
    "email": "mike@gamma.com",
    "phone": "555-3456"
}

customer4 = {
    "company_name": "Delta Tech",
    "contact_person": "Sarah Lee",
    "email": "sarah@deltatech.com",
    "phone": "555-4567"
}

# TODO 3: Master customers dictionary
customers = {
    "C001": customer1,
    "C002": customer2,
    "C003": customer3,
    "C004": customer4
}

# TODO 4: Display all customers
print("\nAll Customers:")
print("-" * 60)

for cid, info in customers.items():
    print(cid, info)

# TODO 5: Look up customers
print("\n\nCustomer Lookups:")
print("-" * 60)

c002_info = customers["C002"]
print("C002 info:", c002_info)

c003_contact = customers["C003"]["contact_person"]
print("C003 contact:", c003_contact)

c999_info = customers.get("C999", "Customer not found")
print("C999 lookup:", c999_info)

# TODO 6: Update customer information
customers["C001"]["phone"] = "555-9999"
customers["C002"]["industry"] = "Finance"

print("\n\nUpdating Customer Information:")
print("-" * 60)

for cid, info in customers.items():
    print(cid, info)

# TODO 7: Project dictionaries
project1 = {"name": "Website Revamp", "service": "Web Development", "hours": 120, "budget": 18000}
project2 = {"name": "Security Audit", "service": "Cybersecurity", "hours": 60, "budget": 13200}
project3 = {"name": "Sales Dashboard", "service": "Data Analysis", "hours": 80, "budget": 14000}
project4 = {"name": "Cloud Migration", "service": "Cloud Consulting", "hours": 100, "budget": 20000}
project5 = {"name": "Helpdesk Setup", "service": "IT Support", "hours": 40, "budget": 3600}

projects = {
    "C001": [project1, project2],
    "C002": [project3],
    "C003": [project4],
    "C004": [project5]
}

print("\n\nProject Information:")
print("-" * 60)

for cid, plist in projects.items():
    print(cid, plist)

# TODO 8: Project costs
print("\n\nProject Cost Calculations:")
print("-" * 60)

for cid, plist in projects.items():
    for p in plist:
        rate = services[p["service"]]
        cost = rate * p["hours"]
        print(p["name"], "Cost:", cost)

# TODO 9: Customer statistics
print("\n\nCustomer Statistics:")
print("-" * 60)

print("Customer IDs:", customers.keys())

companies = [c["company_name"] for c in customers.values()]
print("Customer companies:", companies)

print("Total customers:", len(customers))

# TODO 10: Service usage
service_counts = {}

for plist in projects.values():
    for p in plist:
        s = p["service"]
        service_counts[s] = service_counts.get(s, 0) + 1

print("\n\nService Usage Analysis:")
print("-" * 60)
print(service_counts)

# TODO 11: Financial aggregations
all_hours = []
all_budgets = []

for plist in projects.values():
    for p in plist:
        all_hours.append(p["hours"])
        all_budgets.append(p["budget"])

total_hours = sum(all_hours)
total_budget = sum(all_budgets)
avg_budget = total_budget / len(all_budgets)
max_budget = max(all_budgets)
min_budget = min(all_budgets)

print("\n\nFinancial Summary:")
print("-" * 60)

print("Total hours:", total_hours)
print("Total budget:", total_budget)
print("Average budget:", avg_budget)
print("Max project budget:", max_budget)
print("Min project budget:", min_budget)

# TODO 12: Customer summary report
print("\n\nCustomer Summary Report:")
print("-" * 60)

for cid, info in customers.items():
    plist = projects.get(cid, [])
    hours = sum(p["hours"] for p in plist)
    budget = sum(p["budget"] for p in plist)

    print(cid, info["company_name"])
    print("Projects:", len(plist))
    print("Total hours:", hours)
    print("Total budget:", budget)
    print()

# TODO 13: Rate adjustments
adjusted_rates = {service: rate * 1.1 for service, rate in services.items()}

print("\n\nAdjusted Service Rates (10% increase):")
print("-" * 60)
print(adjusted_rates)

# TODO 14: Filter customers with projects
active_customers = {cid: customers[cid] for cid in projects if projects[cid]}

print("\n\nActive Customers (with projects):")
print("-" * 60)
print(active_customers)

# TODO 15: Project summaries
customer_budgets = {
    cid: sum(p["budget"] for p in plist)
    for cid, plist in projects.items()
}

print("\n\nCustomer Budget Totals:")
print("-" * 60)
print(customer_budgets)

# TODO 16: Service tiers
service_tiers = {
    service: "Premium" if rate >= 200 else "Standard" if rate >= 100 else "Basic"
    for service, rate in services.items()
}

print("\n\nService Pricing Tiers:")
print("-" * 60)
print(service_tiers)

# TODO 17: Customer validation
def validate_customer(customer_dict):
    required = ["company_name", "contact_person", "email", "phone"]
    for field in required:
        if field not in customer_dict:
            return False
    return True

print("\n\nCustomer Validation:")
print("-" * 60)

for cid, info in customers.items():
    print(cid, validate_customer(info))

# TODO 18: Project status tracking
statuses = ["active", "completed", "pending"]
status_counts = {"active": 0, "completed": 0, "pending": 0}

i = 0
for plist in projects.values():
    for p in plist:
        p["status"] = statuses[i % 3]
        status_counts[p["status"]] += 1
        i += 1

print("\n\nProject Status Summary:")
print("-" * 60)
print(status_counts)

# TODO 19: Budget analysis function
def analyze_customer_budgets(projects_dict):

    result = {}

    for cid, plist in projects_dict.items():

        total = sum(p["budget"] for p in plist)
        count = len(plist)
        average = total / count if count > 0 else 0

        result[cid] = {
            "total": total,
            "average": average,
            "count": count
        }

    return result

print("\n\nDetailed Budget Analysis:")
print("-" * 60)

budget_stats = analyze_customer_budgets(projects)
print(budget_stats)

# TODO 20: Service recommendation system
def recommend_services(customer_id, customers, projects, services):

    used_services = set()

    for p in projects.get(customer_id, []):
        used_services.add(p["service"])

    recommendations = []

    for s in services:
        if s not in used_services:
            recommendations.append(s)

    return recommendations

print("\n\nService Recommendations:")
print("-" * 60)

print("Recommendations for C001:", recommend_services("C001", customers, projects, services))