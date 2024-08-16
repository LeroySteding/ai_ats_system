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

import { type ItemPublic, JobsService, type UserPublic } from "../../client"
import AddJob from "../../components/Admin/AddJob"
import ActionsMenu from "../../components/Common/ActionsMenu"
import Navbar from "../../components/Common/Navbar"

const jobsSearchSchema = z.object({
  page: z.number().catch(1),
})

export const Route = createFileRoute("/_layout/jobs")({
  component: Jobs,
  validateSearch: (search) => jobsSearchSchema.parse(search),
})

const PER_PAGE = 5

function getJobsQueryOptions({ page }: { page: number }) {
  return {
    queryFn: () =>
      JobsService.readJobs({ skip: (page - 1) * PER_PAGE, limit: PER_PAGE }),
    queryKey: ["jobs", { page }],
  }
}

function JobsTable() {
  const queryClient = useQueryClient()
  const { page } = Route.useSearch()
  const navigate = useNavigate({ from: Route.fullPath })
  const setPage = (page: number) =>
    navigate({ search: (prev: any) => ({ ...prev, page }) })

  const {
    data: jobs,
    isPending,
    isPlaceholderData,
  } = useQuery({
    ...getJobsQueryOptions({ page }),
    placeholderData: (prevData) => prevData,
  })

  const hasNextPage = !isPlaceholderData && jobs?.data.length === PER_PAGE
  const hasPreviousPage = page > 1

  useEffect(() => {
    if (hasNextPage) {
      queryClient.prefetchQuery(getJobsQueryOptions({ page: page + 1 }))
    }
  }, [page, queryClient, hasNextPage])

  return (
    <>
      <TableContainer>
        <Table size={{ base: "sm", md: "md" }}>
          <Thead>
            <Tr>
              <Th>ID</Th>
              <Th>Title</Th>
              <Th>Description</Th>
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
              {jobs?.data.map((job) => (
                <Tr key={job.id} opacity={isPlaceholderData ? 0.5 : 1}>
                  <Td>{job.id}</Td>
                  <Td isTruncated maxWidth="150px">
                    {job.title}
                  </Td>
                  <Td
                    color={!job.description ? "ui.dim" : "inherit"}
                    isTruncated
                    maxWidth="150px"
                  >
                    {job.description || "N/A"}
                  </Td>
                  <Td>
                    <ActionsMenu
                      type="Job"
                      value={job as ItemPublic | UserPublic}
                    />
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

function Jobs() {
  return (
    <Container maxW="full">
      <Heading size="lg" textAlign={{ base: "center", md: "left" }} pt={12}>
        Jobs Management
      </Heading>

      <Navbar type={"Job"} addModalAs={AddJob} />
      <JobsTable />
    </Container>
  )
}
