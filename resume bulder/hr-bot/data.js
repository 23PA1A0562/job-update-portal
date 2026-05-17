const employees = [
  {
    id: "EMP001",
    name: "John Doe",
    gender: "Male",
    role: "Software Engineer",
    avatar: "https://i.pravatar.cc/150?u=a042581f4e29026024d",
    credentials: {
      wifi: "HRC_Network_2026",
      wifiPass: "S0ftw@reR0cks!"
    },
    leaveBalance: {
      paid: 20,
      casual: 10,
      maternity: 0
    },
    leaveRecord: [
      { type: "casual", date: "2026-03-15", days: 1, status: "approved" }
    ],
    performance: {
      rating: 4.8,
      completedProjects: 12,
      currentProject: {
        name: "JobTracker Pro v2",
        progress: 75,
        deadline: "2026-06-30"
      }
    }
  },
  {
    id: "EMP002",
    name: "Alice Smith",
    gender: "Female",
    role: "Product Manager",
    avatar: "https://i.pravatar.cc/150?u=a042581f4e29026704d",
    credentials: {
      wifi: "HRC_Network_2026",
      wifiPass: "Pr0ductM@gic!"
    },
    leaveBalance: {
      paid: 18,
      casual: 8,
      maternity: 180
    },
    leaveRecord: [
      { type: "paid", date: "2026-01-10", days: 2, status: "approved" }
    ],
    performance: {
      rating: 4.9,
      completedProjects: 20,
      currentProject: {
        name: "Q3 Roadmap Planning",
        progress: 90,
        deadline: "2026-05-25"
      }
    }
  },
  {
    id: "EMP003",
    name: "Michael Johnson",
    gender: "Male",
    role: "UX Designer",
    avatar: "https://i.pravatar.cc/150?img=11",
    credentials: {
      wifi: "HRC_Network_2026",
      wifiPass: "D3signM@sters!"
    },
    leaveBalance: {
      paid: 20,
      casual: 10,
      maternity: 0
    },
    leaveRecord: [],
    performance: {
      rating: 4.5,
      completedProjects: 8,
      currentProject: {
        name: "Dashboard Redesign",
        progress: 40,
        deadline: "2026-07-15"
      }
    }
  }
];

// Using a new storage key to avoid conflicts with previous version
let appState = JSON.parse(localStorage.getItem('hrBotStateV2'));

if (!appState) {
    appState = {
        employees: employees
    };
    localStorage.setItem('hrBotStateV2', JSON.stringify(appState));
}

function saveState() {
    localStorage.setItem('hrBotStateV2', JSON.stringify(appState));
}
