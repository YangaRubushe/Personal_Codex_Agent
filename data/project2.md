# CineNex
![cinenexlogo](https://github.com/YangaRubushe/CineNex/assets/118383164/bc513bc1-348d-4f8f-9442-7de32a7a76a9)

## Overview

[**CineNex**](https://cinenex.vercel.app/) is a modern, user-friendly movie streaming platform inspired by Netflix. The platform features movie trailers and a comprehensive database of movies. Built using cutting-edge technologies such as Next.js 14, Prisma, Supabase, and Shadcn UI, CineNex aims to deliver a seamless and visually appealing user experience.


## CineNex Landing Page:
![image](https://github.com/YangaRubushe/cinenex-landingpage/assets/118383164/4a99364c-629d-4a72-8398-e16d86e54723)

## CineNex LogIn Page:
![image](https://github.com/YangaRubushe/cinenex-landingpage/assets/118383164/8bedd662-3751-4fd8-ad39-9e187f1c9acb)

## CineNex Home Page:
![image](https://github.com/YangaRubushe/cinenex-landingpage/assets/118383164/bfe4189c-ebe7-4ae1-9fd2-1ed029b0eb75)

## Features

- **Trailer Streaming**: Watch high-quality trailers for the latest movies.
- **User Authentication**: Secure login options using Google, GitHub, and email.
- **Responsive Design**: Optimized for viewing on all devices.
- **Dynamic UI**: Beautiful and responsive UI components from Shadcn UI and React.
- **Movie Database**: Comprehensive movie database managed via Prisma and Supabase.

## Technologies Used

- **Next.js 14**: A powerful React framework for server-side rendering and static site generation.
  - [Next.js](https://nextjs.org/)
- **Auth-Next**: A flexible authentication library for Next.js, providing secure authentication options.
  - [NextAuth.js](https://next-auth.js.org/)
- **Prisma**: An ORM for Node.js and TypeScript, used for database management and migrations.
  - [Prisma](https://www.prisma.io/)
- **Supabase**: An open-source Firebase alternative, used as the backend database.
  - [Supabase](https://supabase.com/)
- **Shadcn UI**: A modern, beautiful UI library used to build the frontend components.
  - [Shadcn UI](https://shadcn.dev/)
- **Vercel**: Deployment platform for frontend applications, used to host CineNex.
  - [Vercel](https://vercel.com/)

## Installation

To set up CineNex locally, follow these steps:

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/YangaRubushe/CineNex.git
   cd CineNex
   ```

2. **Install Dependencies**:
   Ensure you have `npm` and `Next.js` installed, then run:
   ```sh
   npm install
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory and add your personal information, including API keys. Here's an example of what you might need:
   ```env
   DATABASE_URL=<your-database-url>
   NEXTAUTH_URL=<your-next-auth-url>
   GOOGLE_CLIENT_ID=<your-google-client-id>
   GOOGLE_CLIENT_SECRET=<your-google-client-secret>
   GITHUB_CLIENT_ID=<your-github-client-id>
   GITHUB_CLIENT_SECRET=<your-github-client-secret>
   ```

4. **Run the Development Server**:
   Start the development server with:
   ```sh
   npm run dev
   ```

   Your application should now be running on `http://localhost:3000`.

## Deployment

CineNex is deployed using Vercel. To deploy your own version:

1. **Connect to Vercel**: Log in to Vercel and connect your GitHub repository.
2. **Configure Environment Variables**: Set the same environment variables in Vercel as you have in your local `.env` file.
3. **Deploy**: Trigger a deployment from the Vercel dashboard.

## Usage

- **Browse Movies**: Explore the latest movie trailers and detailed information about each movie.
- **Authentication**: Sign up or log in using Google, GitHub, or email for a personalized experience.
- **Responsive Design**: Enjoy a seamless experience across all devices.

## Contributing

Developers are welcome to contribute to CineNex. To get started:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or feedback, please contact:

- **Name**: Yanga Rubushe
- **GitHub**: [YangaRubushe](https://github.com/YangaRubushe)
- **X**: [YangaRubushe](https://x.com/YangaRubushe)

---

Thank you for using [CineNex](https://cinenex.vercel.app/)! Enjoy streaming the latest movie trailers.
