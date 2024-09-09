document.getElementById("get-users").addEventListener("click", function() {
    console.log("Button clicked");
    fetch("/users/")
    .then(response => response.json())
    .then(data => {
        const users = data.users;
        const root = document.getElementById("root");
        root.innerHTML = "";
        users.forEach(user => {
            const userDiv = document.createElement("div");
            userDiv.classList.add("card", "mb-5");
            userDiv.style.width = "18rem";
            userDiv.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${user.username}</h5>
                    <p class="card-text">Name: ${user.first_name} ${user.last_name}</p>
                    <p class="card-text">Email: ${user.email}</p>
                    <p class="card-text">Phone: ${user.phone_number}</p>
                    <p class="card-text">Address: ${user.address}</p>
                    <p class="card-text">City: ${user.city}</p>
                    <p class="card-text">Zip: ${user.CP}</p>
                    <button class="btn btn-primary" onclick="window.location.href='/profile/${user.username}'">View</button>
                    <button class="btn btn-danger" onclick="window.location.href='/profile/${user.username}/delete'">Delete</button>
                </div>
            `;
            root.appendChild(userDiv);
        });
    });
});

document.getElementById("get-cars").addEventListener("click", function() {
    console.log("Button clicked");
    fetch("/cars/")
    .then(response => response.json())
    .then(data => {
        const cars = data.cars;
        const root = document.getElementById("root");
        root.innerHTML = "";
        cars.forEach(car => {
            const carDiv = document.createElement("div");
            carDiv.classList.add("card", "mb-5");
            carDiv.style.width = "18rem";
            carDiv.innerHTML = `
                <div class="card-body">
                    <img src="/images/${car.image1}" class="card-img-top" alt="...">
                    <p class="card-text">Year: ${car.year}</p>
                    <p class="card-text">Price: ${car.price}</p>
                    <p class="card-text">License Plate: ${car.licence_plate}</p>
                    <button class="btn btn-primary" onclick="window.location.href='/car/${car.licence_plate}'">View</button>
                </div>
            `;
            root.appendChild(carDiv);
            }
        );
    });
});

const clearBtn = document.getElementById("clear").addEventListener("click", function() {
    console.log("Root clear");
    const root = document.getElementById("root");
    root.innerHTML = "";
});
;


/* document.getElementById("get-bookings").addEventListener("click", function() {
    console.log("Button clicked");
    fetch("/bookings/")
    .then(response => {
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.bookings) {
            const bookings = data.bookings;
            const root = document.getElementById("root");
            root.innerHTML = "";
            bookings.forEach(booking => {
                const bookingDiv = document.createElement("div");
                bookingDiv.classList.add("card", "mb-5");
                bookingDiv.style.width = "18rem";
                bookingDiv.innerHTML = `
                    <div class="card-body">
                        <h5 class="card-title">Booking by: ${booking.user__username}</h5>
                        <p class="card-text">Car: ${booking.car__name}</p>
                        <p class="card-text">Start Date: ${booking.start_date}</p>
                        <p class="card-text">Total Price: $${booking.total_price}</p>
                        <button class="btn btn-primary" onclick="window.location.href='/booking/${booking.id}'">View</button>
                        <button class="btn btn-danger" onclick="window.location.href='/booking/${booking.id}/delete'">Delete</button>
                    </div>
                `;
                root.appendChild(bookingDiv);
            });
        } else {
            console.error("Bookings data not found.");
        }
    })
    .catch(error => console.error("Error fetching data:", error));
});
 */