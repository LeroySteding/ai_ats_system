import {
  Button,
  Container,
  Flex,
  Heading,
  SkeletonText,
  Table,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from "@chakra-ui/react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { createFileRoute, useNavigate } from "@tanstack/react-router"
import { useEffect } from "react"
import { z } from "zod"

import AddProfile from "../../components/Admin/AddProfile"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

import { ProfilesService } from "../../client"

const profilesSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/profiles")({
  component: Profiles,
  validateSearch: (search) => profilesSearchSchema.parse(search),
})

const PER_PAGE = 5

function getProfilesQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      ProfilesService.readProfiles({
        skip: (page - 1) * PER_PAGE,
        limit: PER_PAGE,
      }),
    queryKey: ["profiles", { page }],
  }
}

function ProfilesTable() {
  const queryClient = useQueryClient()
  const { page } = Route.useSearch()
  const navigate = useNavigate({ from: Route.fullPath })
  const setPage = (page: number) =>
    navigate({ search: (prev: any) => ({ ...prev, page }) })

  const {
    data: profiles,
    isPending,
    isPlaceholderData,
  } = useQuery({
    ...getProfilesQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const hasNextPage = !isPlaceholderData && profiles?.data.length === PER_PAGE
  const hasPreviousPage = page > 1

  useEffect(() => {
    if (hasNextPage) {
      queryClient.prefetchQuery(getProfilesQueryOptions({ page: page + 1 }))
    }
  }, [page, queryClient, hasNextPage])

  return (
    <>
      <TableContainer>
        <Table size={{ base: "sm", md: "md" }}>
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>Full Name</Th>
              <Th>Bio</Th>
              <Th>Actions</Th>
            </Tr>
          </Thead>
          {isPending ? (
            <Tbody>
              <Tr>
                {new Array(4).fill(null).map((_, index) => (
                  <Td key={index}>
                    <SkeletonText noOfLines={1} paddingBlock="16px" />
                  </Td>
                ))}
              </Tr>
            </Tbody>
          ) : (
            <Tbody>
              {profiles?.data.map((profile) => (
                <Tr key={profile.id} opacity={isPlaceholderData ? 0.5 : 1}>
                  <Td>{profile.id}</Td>
                  <Td isTruncated maxWidth="150px">
                    {profile.full_name}
                  </Td>
                  <Td
                    color={!profile.status ? "ui.dim" : "inherit"}
                    isTruncated
                    maxWidth="150px"
                  >
                    {profile.role || "N/A"}
                  </Td>
                  <Td>
                    <ActionsMenu type={"Profile"} value={profile} />
                  </Td>
                </Tr>
              ))}
            </Tbody>
          )}
        </Table>
      </TableContainer>
      <Flex
        gap={4}
        alignItems="center"
        mt={4}
        direction="row"
        justifyContent="flex-end"
      >
        <Button onClick={() => setPage(page - 1)} isDisabled={!hasPreviousPage}>
          Previous
        </Button>
        <span>Page {page}</span>
        <Button isDisabled={!hasNextPage} onClick={() => setPage(page + 1)}>
          Next
        </Button>
      </Flex>
    </>
  )
}

function Profiles() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        Profiles Management
      </Heading>

      <Navbar type={"Profile"} addModalAs={AddProfile} />
      <ProfilesTable />
    </Container>
  )
}
