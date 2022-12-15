import prisma from './lib/utils/prisma';

export const handle = async ({ event, resolve }) => {
	const session = event.cookies.get('session');

	// If no session exists, return the normal page
	if (!session) return await resolve(event);

	// Find the user with the unique id (which also is the session)
	const user = await prisma.users.findUnique({
		where: {
			id: session
		}
	});

	if (user) event.locals.user = user;

	return await resolve(event);
};